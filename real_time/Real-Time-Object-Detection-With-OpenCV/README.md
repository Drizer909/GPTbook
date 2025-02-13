# Real-Time Object Detection and Gesture Recognition

> ⚠️ **IMPORTANT NOTICE**: This repository will be archived on `February 16, 2024`. Please fork or download before this date.

A computer vision project that combines real-time object detection and hand gesture recognition using OpenCV and MediaPipe.

## Features

- Real-time object detection using MobileNet SSD
- Hand gesture recognition (thumbs up, OK sign, heart shape)
- Multi-object detection with confidence scores
- FPS counter and performance metrics
- Live webcam feed processing

## Technologies Used

- Python
- OpenCV
- MediaPipe
- MobileNet SSD (Single Shot MultiBox Detector)
- NumPy
- Imutils

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Drizer909/Real-Time-Object-Detection.git
cd Real-Time-Object-Detection
```

2. Install required packages:
```bash
pip install opencv-python
pip install opencv-contrib-python
pip install imutils
pip install mediapipe
```

## Usage

### For Basic Object Detection:
```bash
python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
```

### For Object Detection with Hand Gestures:
```bash
python gesture_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
```

## Supported Detections

### Objects:
- Person
- Car
- Chair
- Bottle
- And many more...

### Gestures:
- Thumbs Up 👍
- OK Sign 👌
- Heart Shape ❤️

## Controls
- Press 'q' to quit the application
- The window shows:
  - FPS counter (top-left)
  - Detected objects with confidence scores
  - Recognized hand gestures (in gesture version)

## Project Structure
```
Real-Time-Object-Detection/
├── real_time_object_detection.py    # Basic object detection
├── gesture_object_detection.py      # Enhanced version with gestures
├── MobileNetSSD_deploy.caffemodel  # Pre-trained model
└── MobileNetSSD_deploy.prototxt.txt # Model configuration
```

## Results
- Achieves 30+ FPS on standard hardware
- Real-time object detection with 80%+ accuracy
- Gesture recognition with sub-100ms latency

Note: This repository will be available for 3 days from the date of creation.

Made by Shivam Sharma 