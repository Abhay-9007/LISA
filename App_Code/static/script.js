// static/script.js

// ─── DOM refs ────────────────────────────────────────────────────────────────
const chat        = document.getElementById("chat");
const msgInput    = document.getElementById("msg");
const sendBtn     = document.getElementById("send");
const micBtn      = document.getElementById("mic");
const ttsToggle   = document.getElementById("ttsToggle");
const driveToggle = document.getElementById("driveToggle");

// ─── State ───────────────────────────────────────────────────────────────────
let wakeRecognition    = null;
let commandRecognition = null;
let drivingMode        = false;
let waitingForCommand  = false;

// ─── UI helpers ──────────────────────────────────────────────────────────────
function appendBubble(text, who = "bot") {
    const el = document.createElement("div");
    el.classList.add("bubble", who === "user" ? "user" : "bot");
    el.textContent = text;
    chat.appendChild(el);
    chat.scrollTop = chat.scrollHeight;
}

function speakText(text) {
    try {
        if (!("speechSynthesis" in window)) return;
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = "en-US";
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utter);
    } catch (e) {
        console.warn("TTS failed", e);
    }
}

// ─── Open URL without being blocked by popup blocker ─────────────────────────
function openURL(url) {
    const a = document.createElement("a");
    a.href   = url;
    a.target = "_blank";
    a.rel    = "noopener noreferrer";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// ─── Send message to server ──────────────────────────────────────────────────
async function sendMessage(text, WHO="bot") {
    if (!text) return;
    if (WHO !== "code"){
        appendBubble(text, "user");
    }
    try {
        const res  = await fetch("/api", {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ q: text }),
        })
        const data = await res.json();

        if (!data || !data.response) {
            appendBubble(data?.error ? "Error: " + data.error : "No response from server.", "bot");
            return;
        }

        const reply = data.response;

        // Handle special command responses
        if (reply.includes("Searching")) {
            const query = encodeURIComponent(reply.replace("Searching for", "").trim());
            openURL("https://google.com/search?q=" + query);
        } else if (reply.includes("Monolog")) {
            openURL("https://abhay907.pythonanywhere.com/");
        } else if (reply.includes("Playing")) {
            const query = encodeURIComponent(reply.replace("Playing", "").trim());
            openURL("https://www.youtube.com/results?search_query=" + query);
        } else if (reply.includes("Opening")) {
            if      (reply.includes("Instagram")) openURL("https://www.instagram.com/");
            else if (reply.includes("YouTube"))   openURL("https://www.youtube.com/");
            else if (reply.includes("ChatGPT"))   openURL("https://www.chatgpt.com/");
            else {
                const site = encodeURIComponent(reply.replace("Opening", "").trim());
                openURL("https://www." + site + ".com/");
            }
        }

        // Display response & speak if TTS is on
        appendBubble(reply, "bot");
        if (ttsToggle.checked) speakText(reply);

    } catch (e) {
        appendBubble("Network error.", "bot");
        console.error(e);
    }
}

// ─── UI events ───────────────────────────────────────────────────────────────
sendBtn.addEventListener("click", () => {
    const t = msgInput.value.trim();
    if (!t) return;
    msgInput.value = "";
    sendMessage(t);
});

msgInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendBtn.click();
});

micBtn.addEventListener("click", () => {
    if (!commandRecognition) {
        appendBubble("Voice not supported in this browser.", "bot");
        return;
    }
    try { commandRecognition.start(); }
    catch (err) { console.warn(err); }
});

driveToggle.addEventListener("change", () => {
    drivingMode = driveToggle.checked;
    if (drivingMode) {
        appendBubble("🚗 Driving Mode Activated", "bot");
        speakText("Driving mode activated");
        try { wakeRecognition.start(); } catch (err) { console.warn(err); }
    } else {
        appendBubble("🚗 Driving Mode Deactivated", "bot");
        speakText("Driving mode deactivated");
        try { wakeRecognition.stop(); } catch (err) { console.warn(err); }
        waitingForCommand = false;
    }
});

// ─── Speech recognition ──────────────────────────────────────────────────────
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

    // Wake word listener
    wakeRecognition               = new SR();
    wakeRecognition.continuous    = true;
    wakeRecognition.interimResults = true;
    wakeRecognition.lang          = "en-US";

    // Command listener
    commandRecognition                  = new SR();
    commandRecognition.continuous       = false;
    commandRecognition.interimResults   = false;
    commandRecognition.maxAlternatives  = 1;
    commandRecognition.lang             = "en-US";

    // Wake word detected
    wakeRecognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0]
            .transcript.toLowerCase().trim();

        console.log("WAKE:", transcript);

        if (transcript.includes("lisa") && !waitingForCommand) {
            waitingForCommand = true;
            appendBubble("🎙 Listening...", "bot");

            try { wakeRecognition.stop(); } catch (err) { console.warn(err); }

            speakText("Yes Sir");

            setTimeout(() => {
                try { commandRecognition.start(); } catch (err) { console.warn(err); }
            }, 1000);
        }
    };

    // Command received
    commandRecognition.onresult = async (event) => {
        const command = event.results[0][0].transcript;
        console.log("COMMAND:", command);

        waitingForCommand = false;
        await sendMessage(command);  // wait for fetch + openURL before restarting wake

        if (drivingMode) {
            setTimeout(() => {
                try { wakeRecognition.start(); } catch (err) { console.warn(err); }
            }, 1000);
        }
    };

    // Command failed / no speech
    commandRecognition.onerror = (event) => {
        console.warn("COMMAND ERROR:", event.error);
        waitingForCommand = false;
        if (drivingMode) {
            setTimeout(() => {
                try { wakeRecognition.start(); } catch (err) {}
            }, 500);
        }
    };

    commandRecognition.onend = () => {
        console.log("COMMAND ENDED");
        if (drivingMode && !waitingForCommand) {
            setTimeout(() => {
                try { wakeRecognition.start(); } catch (err) {}
            }, 500);
        }
    };

    // Wake listener ended — restart in driving mode
    wakeRecognition.onend = () => {
        console.log("WAKE ENDED");
        if (drivingMode && !waitingForCommand) {
            setTimeout(() => {
                try { wakeRecognition.start(); } catch (err) {}
            }, 500);
        }
    };

} else {
    appendBubble("Speech recognition not supported in this browser.", "bot");
}

// ─── Notifications ───────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    if ("Notification" in window) {
        Notification.requestPermission();
        startScheduler();
    }
});

function showNotification() {
    if (Notification.permission === "granted") {
        new Notification("⏰ Reminder", { body: "Don't waste time..." });
    }
}

function startScheduler() {
    function checkTimeAndNotify() {
        const hours = new Date().getHours();
        if (hours >= 8 && hours <= 24) showNotification();
    }
    checkTimeAndNotify();
    setInterval(checkTimeAndNotify, 60 * 60 * 1000);
}

// ─── Welcome ─────────────────────────────────────────────────────────────────
appendBubble("Hey! How can I help?", "bot");
sendMessage("give me home reminder", "code");
