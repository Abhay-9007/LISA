[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage (relative to spec file)
build_dir = ./.buildozer

# (str) Path to build output (APK storage)
bin_dir = ./bin

# -----------------------------------------------------------------------------
# Application information
# -----------------------------------------------------------------------------
[app]

# (str) Title of your application
title = LISA App

# (str) Package name
package.name = lisaapp

# (str) Package domain (must be unique, usually reversed domain)
package.domain = org.abhay

# (str) Source code folder
source.dir = .

# (str) Main .py file
source.main = main.py

# (list) Application requirements (add any extra Python libraries here)
requirements = python3,kivy,requests

# (str) Supported orientation: portrait, landscape
orientation = portrait

# (bool) Fullscreen
fullscreen = 1

# -----------------------------------------------------------------------------
# Android settings
# -----------------------------------------------------------------------------
[buildozer:android]

# (int) Target Android API
android.api = 34

# (int) Minimum supported Android API
android.minapi = 21

# (str) Android SDK version
android.sdk = 34

# (str) Android NDK version
android.ndk = 25b

# (str) Android bootstrap
android.bootstrap = sdl2

# (list) Android architectures to build for
android.arch = arm64-v8a,armeabi-v7a

# (bool) Copy shared libraries into the APK
android.copy_libs = 1

# -----------------------------------------------------------------------------
# iOS settings (optional, you can leave empty)
# -----------------------------------------------------------------------------
[ios]

# -----------------------------------------------------------------------------
# Other sections can remain default
# -----------------------------------------------------------------------------
