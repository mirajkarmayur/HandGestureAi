# Hand Gesture AI Volume Controller

A real-time hand gesture-based volume controller built with Python, OpenCV, MediaPipe, and Pycaw.

## Features

- Real-time hand detection using MediaPipe
- Gesture recognition using hand landmarks
- Windows volume control using hand gestures
- Volume increase and decrease in 5% steps
- Gesture stabilization to reduce accidental actions
- Hand landmark visualization
- Real-time volume indicator
- Mute and unmute control
- FPS display


## Gesture Controls

 ✊ Fist → ☝️ Index finger >> Increase volume by 5% 

 
 ✊ Fist → ✌️ Peace pose   >> Decrease volume by 5% 

 
 🖐️ Open hand              >> Toggle mute / unmute   

 
## Technologies Used

- **Python** — Main programming language
- **OpenCV** — Camera capture, image processing, and user interface
- **MediaPipe** — Real-time hand landmark detection
- **Pycaw** — Windows audio volume control
- **Comtypes** — Windows audio interface support



## Installation

### 1. Clone the repository
git clone <your-repository-url>
cd HandAI
### 2. Install the required libraries
pip install -r requirements.txt
### 3. Run the application
python main.py



## Project Structure

HandAI



│


├── main.py                    # Main application

├── config.py                  # Project configuration

├── gesture_detector.py        # Hand gesture detection

├── hand_controller.py         # Windows volume control

├── test_volume.py              # Audio control test

├── hand_landmarker.task        # MediaPipe hand model

├── requirements.txt            # Python dependencies

├── .gitignore                 # Files ignored by Git

└── README.md                  # Project documentation



## How It Works

1. The webcam captures a live video feed.
2. OpenCV processes each camera frame.
3. MediaPipe detects the hand and identifies its 21 landmarks.
4. The gesture detector analyzes the landmark positions to identify the gesture.
5. Gesture stabilization checks multiple frames to reduce accidental actions.
6. The detected gesture is passed to the volume controller.
7. Pycaw communicates with Windows to change the system volume or mute status.
8. OpenCV displays the camera feed, detected gesture, volume level, and FPS.


## Usage

1. Connect a working webcam to your computer.
2. Run the application using:
python main.py
3. Position your hand in front of the camera.
4. Use the gestures shown below:
 ✊ Fist → ☝️ Index finger >> Increase volume by 5% 
 ✊ Fist → ✌️ Peace pose   >> Decrease volume by 5% 
 🖐️ Open hand              >> Toggle mute / unmute   
5. Press `Q` to close the application.


## Requirements / Notes

- Windows operating system
- Python 3.x
- Working webcam
- Internet connection for installing Python dependencies
- `hand_landmarker.task` must be present in the project directory
- The project uses Pycaw for Windows system volume control



## Future Improvements

- Add more customizable hand gestures
- Support application-specific volume control
- Add a graphical settings interface
- Improve gesture recognition for different hand orientations
- Add support for additional operating systems
- Add configurable volume step sizes
