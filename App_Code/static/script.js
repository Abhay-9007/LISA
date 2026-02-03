// static/script.js
const chat = document.getElementById("chat");
const msgInput = document.getElementById("msg");
const sendBtn = document.getElementById("send");
const micBtn = document.getElementById("mic");
const ttsToggle = document.getElementById("ttsToggle");

function appendBubble(text, who="bot") {
    const el = document.createElement("div");
    el.classList.add("bubble", who === "user" ? "user" : "bot");
    el.textContent = text;
    chat.appendChild(el);
    chat.scrollTop = chat.scrollHeight;
}

// send message to server API
async function sendMessage(text) {
    console.log("Sending message:", text);
    if (!text) return;
    appendBubble(text, "user");
    
    try {
        const res = await fetch("/api", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({ q: text })
        });
        const data = await res.json();
        // console.log(res);
        // console.log(data);
        if (data.response.includes("Searching")){
            content = data.response.replace("Searching for", "").trim();
            window.open("https://google.com/search?q="+ content, "_blank");
        }
        else if (data.response.includes("Monolog")){
            window.open("https://abhay907.pythonanywhere.com/", "_blank");
        }
        else if (data.response.includes("Playing")){
            content = data.response.replace("Playing", "").trim();
            window.open("https://www.youtube.com/results?search_query="+ content, "_blank");
        }
        else if (data.response.includes("Opening")){
            if (data.response.includes("Instagram")){
                window.open("https://www.instagram.com/", "_blank");
                }
                else if (data.response.includes("YouTube")){
                window.open("https://www.youtube.com/", "_blank");
            }
            else if (data.response.includes("ChatGPT")){
                window.open("https://www.chatgpt.com/", "_blank");
            }
            else{
                content = data.response.replace("Opening", "").trim();
                window.open("https://www."+content+".com/", "_blank");
            }
            
        }
        if (data && data.response) {
            //data.response = "Abhay is a boss here: \n gottam is a Nigga";
            appendBubble(data.response, "bot");
            if (ttsToggle.checked && "speechSynthesis" in window) {
                speakText(data.response);
            }
        } else if (data && data.error) {
            appendBubble("Error: " + data.error, "bot");
        } else {
            appendBubble("No response from server.", "bot");
        }
    } catch (e) {
        appendBubble("Network error.", "bot");
        console.error(e);
    }
}

function speakText(text) {
    try {
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = "en-US";
        window.speechSynthesis.cancel(); // stop previous
        window.speechSynthesis.speak(utter);
    } catch (e) {
        console.warn("TTS failed", e);
    }
}

// UI events
sendBtn.addEventListener("click", () => {
    const t = msgInput.value.trim();
    if (t === "") return;
    msgInput.value = "";
    sendMessage(t);
});
msgInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendBtn.click();
    }
});

// Voice input using Web Speech API
let recognition;
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SR();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        msgInput.value = text;
        sendMessage(text);
    };
    recognition.onerror = (e) => {
        console.warn("Speech recognition error", e);
    };
} else {
    recognition = null;
}

micBtn.addEventListener("click", () => {
    if (!recognition) {
        appendBubble("Voice not supported in this browser.", "bot");
        return;
    }
    try {
        recognition.start();
    } catch (e) {
        console.warn(e);
    }
});

// Welcome message
appendBubble("Hello, how can I help you?", "bot");
