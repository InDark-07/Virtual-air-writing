# Virtual Air Writing

A real-time computer vision application that allows users to write and erase on a virtual canvas using hand gestures detected through a webcam.

## Features

* Real-time hand tracking using MediaPipe
* Index-finger drawing
* Two-finger erasing
* Keyboard-based canvas clearing
* Live camera overlay using OpenCV

## Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment using:

```bash
.venv\Scripts\activate
```

## Run the Application

```bash
python main.py
```

## Controls

* Raise the index finger to draw.
* Raise the index and middle fingers to erase.
* Press `C` to clear the canvas.
* Press `Q` to quit.

## Architecture

The application separates hand tracking, gesture recognition, drawing operations, configuration, and application execution into independent modules.

## Limitations

Gesture recognition relies on relative landmark positions. Performance depends on lighting, hand orientation, webcam quality, and the installed dependency versions.



## keyboard shortcuts
C- Clear the entire canvas
S- Save the drawing to drawing.png
=- Increase brush thickness
-- Decrease brush thickness
]- Increase eraser size
[- Decrease eraser size
Q- Quit the application
