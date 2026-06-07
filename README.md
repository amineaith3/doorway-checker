# Corporate Door Entry Simulator (Doorway Checker)

A real-time computer vision application designed to monitor doorways, detecting and tracking employees entering or exiting the premises. Built with Streamlit, OpenCV, and Ultralytics YOLOv11.

## Features

- **YOLOv11 Tracking Engine**: Employs the highly optimized YOLO11 Nano model for lightning-fast inference on standard CPUs.
- **Precision Filtering**: Configured to ignore background noise and detect exclusively "Persons" (COCO Class 0).
- **Persistent Tracking**: Assigns and tracks unique IDs across consecutive frames to prevent duplicate logs.
- **Live Surveillance Log**: Dynamically generates timestamped entry and exit logs (e.g., `[ENTRY] [12s]: Employee ID:3 entered the building`).
- **Clean Architecture**: Separates the backend computer vision logic (`tracker.py`) from the frontend web interface (`app.py`).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amineaith3/doorway-checker.git
   cd doorway-checker
   ```

2. Install the required dependencies:
   ```bash
   pip install streamlit opencv-python ultralytics
   ```

## Usage

Start the Streamlit application by running:
```bash
streamlit run app.py
```

Upload a video of a doorway or hallway into the web UI, and the app will automatically process the video, tracking all entries and exits in real-time.
