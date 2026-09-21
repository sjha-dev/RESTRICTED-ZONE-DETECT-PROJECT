# Restricted Zone Detection System

A Computer Vision-based monitoring system using YOLOv8 and OpenCV to detect unauthorized access in restricted areas and monitor safety compliance in real-time.

---

## Features

- Real-Time Object Detection: Uses YOLOv8 for fast and accurate object tracking.
- Restricted Area Monitoring: Detects human entry or unauthorized movement inside defined spatial boundaries.
- Audio Alerts: Triggers an alert sound when safety violations or unauthorized breaches occur.
- Live Video Feed Processing: Processes video files or live camera feeds with visual bounding boxes and status overlays.

---

## Repository Structure

```text
RESTRICTED-ZONE-DETECT-PROJECT/
├── main.py              # Main detection logic & video processing pipeline
├── requirements.txt     # Python dependencies
├── yolov8n.pt           # YOLOv8 pre-trained model weights
└── README.md            # Project documentation
```

---

## Prerequisites & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/sjha-dev/RESTRICTED-ZONE-DETECT-PROJECT.git
cd RESTRICTED-ZONE-DETECT-PROJECT
```

### 2. Set Up Virtual Environment (Optional)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

Run the main script to start real-time detection:

```bash
python main.py
```

Press 'q' on your keyboard while the video feed window is focused to stop execution.

---

## Built With

- Python: Primary programming language
- OpenCV: Image processing and video stream rendering
- Ultralytics YOLOv8: Object detection and tracking framework
- Pygame / Winsound: Audio alert triggers
