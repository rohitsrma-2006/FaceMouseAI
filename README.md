# FaceMouse AI

FaceMouse AI is a Python desktop application for Windows that lets you control your mouse cursor using a webcam and face movements. It uses computer vision and facial landmark tracking to provide hands-free cursor navigation and blink-based mouse actions.

---

# Features

## Core Controls

* Control mouse cursor using head / face movement
* Full face landmark tracking using webcam
* Cursor smoothing for stable movement
* Calibration mode for accurate center positioning
* Pause / Resume tracking anytime

## Smart Actions

* Quick blink = Left click
* Double blink = Double click
* Long blink = Drag mode toggle
* Recenter tracking with keyboard shortcut

## Interface

* Desktop GUI built with CustomTkinter
* Live webcam preview
* Status indicators

---

# How It Works

FaceMouse AI uses:

* OpenCV for webcam capture
* MediaPipe Face Mesh for facial landmark detection
* PyAutoGUI for mouse control
* CustomTkinter for modern GUI

The system tracks facial movement and converts it into cursor movement.

---

# Project Structure

```text
FaceMouseAI/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   └── app.ico
│
└── src/
    ├── main.py
    ├── ui.py
    ├── tracker.py
    ├── blink.py
    ├── mouse_control.py
    ├── pose.py
    ├── config.py
    └── utils.py
```

---

# Installation (Windows PowerShell)

## 1. Clone Repository

```powershell
git clone https://github.com/yourusername/FaceMouseAI.git
cd FaceMouseAI
```

## 2. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Run Application

## Recommended

```powershell
python main.py
```

## Alternative

```powershell
python src/main.py
```

---

# Controls

| Action       | Result           |
| ------------ | ---------------- |
| Move head    | Move cursor      |
| Quick blink  | Left click       |
| Double blink | Double click     |
| Long blink   | Drag mode on/off |
| Spacebar     | Pause / Resume   |
| R            | Recalibrate      |
| ESC          | Exit camera      |

---

# Calibration

When tracking starts:

1. Sit naturally in front of webcam
2. Look at center of screen
3. Keep head still for a few seconds
4. Tracking begins automatically

For best results:

* Good lighting
* Face clearly visible
* Webcam at eye level
* Sit comfortably

---

# Requirements

* Windows 10 / 11
* Python 3.10+
* Webcam
* 720p webcam recommended

---

# Dependencies

* opencv-python
* mediapipe
* pyautogui
* customtkinter
* pillow
* numpy

Install all using:

```powershell
pip install -r requirements.txt
```

---

# Current Status

This project is an active prototype / MVP with working core features.

Implemented:

* Face tracking
* Cursor movement
* Blink clicking
* Pause mode
* Calibration mode
* Drag mode

---

# Planned Improvements

* Sensitivity slider in GUI
* Save settings
* Better blink accuracy
* Multi-monitor support
* Accessibility profiles
* Lower CPU usage
* Better cursor acceleration
* Linux support
* macOS support

---

# Troubleshooting

## Cursor Too Fast

Adjust sensitivity values in `tracker.py`

## Blink Not Detecting

Improve lighting and face visibility.

## Cursor Shaking

Use stable lighting and keep webcam fixed.

## Webcam Not Opening

Check if another app is using camera.

---

# Git Commands

```powershell
git add .
git commit -m "Updated FaceMouse AI"
git push
```

---

# Disclaimer

FaceMouse AI is an experimental computer vision control system. Performance may vary based on lighting, webcam quality, and system hardware.

---

# License

MIT License

---

# Author

Developed by Rohit Sharma
