# 🎵 Discord Multi-Bot
<p align="center">
  <img src="assets/SX2.png" alt="Discord Multi-Bot Banner" width="600">

<p align="center">
  A powerful **all-in-one Discord bot** featuring:<br>
  🎶 Music • 🔨 Moderation • 🎉 Fun • ℹ️ Info • 🤖 Utilities
</p></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python Badge">
  <img src="https://img.shields.io/badge/Discord.py-2.4.0-blueviolet?logo=discord" alt="Discord.py Badge">
  <img src="https://img.shields.io/badge/Music-Bot-orange?logo=youtube" alt="Music Badge">
</p>


---

## 🚀 Features
- **Music**: Play from YouTube (play, pause, resume, stop, join, leave)  
- **Moderation**: Kick, ban, mute, warn, clear messages  
- **Fun**: Jokes, random quotes  
- **Info**: Server info, user info, bot info  
- **Utility**: Help menu, custom prefixes  

---

## 🛠️ Installation

### 1. Clone this repo
git clone https://github.com/SX2s/discord-multi-bot.git
cd discord-multi-bot

### 2. Install dependencies
pip install -U discord.py yt-dlp PyNaCl

### 3. Install FFmpeg
### 🔧 FFmpeg Setup (Required for Music)

Because GitHub doesn’t allow files > 100 MB, the FFmpeg binaries are *not included* in this repo.  
To get them working:

1. Go to the [FFmpeg official site](https://ffmpeg.org/download.html) or a trusted build provider for Windows.  
2. Download the **Windows build** (look for `.zip` or `.7z` with `ffmpeg.exe`).  
3. Extract it so you see `ffmpeg.exe`, `ffplay.exe`, `ffprobe.exe`.  
4. Place `ffmpeg.exe` in the same folder as `bot.py` (or modify the path in your code).  
5. Run your bot normally — it should find FFmpeg locally and music commands will work.

Make sure `.gitignore` prevents those `.exe` files from being pushed again.

### ⚠️ Important: We don’t store FFmpeg .exe files in GitHub (too large).
### Download FFmpeg from 👉 FFmpeg.org
###  and put ffmpeg.exe in your bot folder (next to bot.py).

### 4. Setup your token

### Create a file called token.txt in the bot folder and paste your Discord bot token inside it.
### 👉 Keep it secret, don’t upload it!

### 📜 Commands
### <details> <summary>🎶 Music</summary>

### !join — Join your voice channel

### !leave — Leave the voice channel

### !play <url> — Play music from YouTube

### !pause — Pause music

### !resume — Resume playback

### !stop — Stop playback

### </details> <details> <summary>🔨 Moderation</summary>

### !kick @user

### !ban @user

### !mute @user

### !warn @user <reason>

### !clear <amount>

### </details> <details> <summary>🎉 Fun</summary>

### !joke

### !quote

### </details> <details> <summary>ℹ️ Info</summary>

### !serverinfo

### !userinfo @user

### !botinfo

### </details>
### 🤝 Contributing

### Pull requests are welcome!
### For major changes, please open an issue first to discuss.

### 📜 License

### MIT License © 2025 SX2s


### ---
