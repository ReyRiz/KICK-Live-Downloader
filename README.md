# 🎥 KickLiveArchiver

<div align="center">

![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge\&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-2B2D42?style=for-the-badge)
![Streamlink](https://img.shields.io/badge/Streaming-Streamlink-FF6B6B?style=for-the-badge)
![FFmpeg](https://img.shields.io/badge/Media-FFmpeg-007808?style=for-the-badge\&logo=ffmpeg)
![PyInstaller](https://img.shields.io/badge/Build-PyInstaller-4B8BBE?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### 🚀 Automatic Kick.com Live Stream Recorder

KickLiveArchiver is a desktop application for automatically monitoring and recording Kick.com live streams with a modern GUI, auto-recording system, and remux support using FFmpeg.

</div>

---

# ✨ Main Features

## 📡 Live Stream Monitoring

* ✅ Automatically monitors Kick.com channel live status
* 🔴 Detects when a streamer goes live
* ⏺️ Starts recording automatically
* 🔁 Continues checking stream status in the background
* 📂 Saves recordings directly to the output folder

---

# 🎬 Recording System

## ⚡ Auto Recording

* Record Kick.com live streams automatically
* Uses Streamlink for reliable stream capture
* Supports high-quality stream recording
* Saves recorded files locally
* Reduces manual checking and recording effort

## 🔄 Remux Support

* Convert or remux recorded files using FFmpeg
* Helps fix video container issues
* Makes recordings easier to play, edit, and archive
* Improves compatibility with media players and editing software

---

# 🖥️ Modern Desktop GUI

KickLiveArchiver comes with a clean desktop interface built using **CustomTkinter**.

## GUI Features

* Modern and simple user interface
* Channel monitoring control
* Recording status display
* Output folder management
* Easy-to-use workflow for non-technical users

---

# 🧰 Tech Stack

| Technology        | Description                              |
| ----------------- | ---------------------------------------- |
| **Python**        | Main programming language                |
| **CustomTkinter** | Modern desktop GUI framework             |
| **Streamlink**    | Stream capture and recording             |
| **FFmpeg**        | Media processing and remuxing            |
| **PyInstaller**   | Build Python app into Windows executable |
| **JSON**          | App configuration storage                |

---

# 🔄 Application Workflow

```text
User Opens App
      ↓
App Loads Configuration
      ↓
Monitor Kick.com Channel
      ↓
Detect Live Status
      ↓
If Channel is Live
      ↓
Start Recording Automatically
      ↓
Save Video to Output Folder
      ↓
Remux File with FFmpeg
      ↓
Recording Ready to Archive
```

---

# 📦 Installation

## 1. Clone Repository

```bash
git clone <repo-url>
cd KickLiveArchiver
```

---

## 2. Create Virtual Environment

Optional, but recommended.

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

Make sure you have **Python 3.8+** installed.

```bash
pip install streamlink customtkinter
```

Required tools:

* Python 3.8+
* Streamlink
* CustomTkinter
* FFmpeg

> FFmpeg binary can be placed inside the `ffmpeg/` folder.

---

# ▶️ Running the App

Run the application using:

```bash
python main.py
```

---

# ⚙️ Configuration

Edit the `config.json` file to adjust the application settings.

Example configuration:

```json
{
  "channel": "example_channel",
  "output_folder": "output",
  "check_interval": 30,
  "quality": "best",
  "auto_remux": true
}
```

## Configuration Options

| Key              | Description                            |
| ---------------- | -------------------------------------- |
| `channel`        | Kick.com channel name to monitor       |
| `output_folder`  | Folder where recordings are saved      |
| `check_interval` | Time interval for checking live status |
| `quality`        | Stream quality, for example `best`     |
| `auto_remux`     | Enable or disable automatic remux      |

---

# 🏗️ Build to EXE

This project supports Windows executable build using **PyInstaller**.

## 1. Install PyInstaller

```bash
pip install pyinstaller
```

## 2. Build Application

```bash
pyinstaller KickLiveArchiver.spec
```

## 3. Build Output

The executable result will be available in:

```text
dist/KickLiveArchiver/
```

---

# 📁 Project Structure

```text
KickLiveArchiver/
│
├── main.py              # Application entry point
├── ui.py                # CustomTkinter user interface
├── monitor.py           # Live status monitoring logic
├── recorder.py          # Recording process handler
├── remux.py             # FFmpeg remux process
├── config.json          # App configuration
├── KickLiveArchiver.spec # PyInstaller build configuration
│
├── ffmpeg/              # FFmpeg binary folder
├── assets/              # Images, icons, and other assets
├── output/              # Recorded video output folder
└── README.md            # Project documentation
```

---

# 📌 Use Case

KickLiveArchiver is useful for:

* Stream archive management
* Content clipping workflow
* Saving live stream sessions automatically
* Reducing manual monitoring
* Creating a local archive for editing and review

---

# ⚠️ Notes

* Make sure your internet connection is stable during recording.
* Recording quality depends on the source stream quality.
* FFmpeg is required for remuxing.
* Use this tool responsibly and respect content ownership, platform rules, and streamer rights.

---

# 🛠️ Future Improvements

* Multi-channel monitoring
* Recording schedule system
* Auto-delete old recordings
* Recording history page
* Telegram or Discord notification
* Better error logging
* Auto-update support

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more details.

---

<div align="center">

### ⭐ KickLiveArchiver

**Automatic Kick.com Live Stream Recorder with GUI and FFmpeg Remux Support**

Made with Python, Streamlink, CustomTkinter, and FFmpeg.

</div>
