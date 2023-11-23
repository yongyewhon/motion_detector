# motion_detector
Save video with time stamp on motion detect (Python).

# Program features
Python implementation to stream camera feed from OpenCV videoCapture via RTSP and record on motion detect.

Motion detected log record with time stamp to track on the motion occur from the "record" folder.

Keep 30 days or can edit from program.

Can set the sensitivity of minimum motion area

# Installation

pip install imutils

# Requirement
Python 3.x

Opencv 3.x or above ( pip install opencv-python )

# Code setting
 
Keep 30 days or can edit from program (eg: Keep_Data = 30) on motion_detector.py line code 17.

Change monitor display resolution (eg: Display_Resolution = (width, height)) on motion_detector.py line code 18

Change record video frame (eg: Video_FPS = 20) on motion_detector.py line code 20

# Usage

python motion_detector.py with required arguments

Try save_rtsp_stream.py --help to view the arguments


optional arguments:

  -h, --help            show this help message and exit
  
  -v VIDEO, --video VIDEO
                        path to the video file
                        
  -a AREA, --area AREA  minimum area size (default=800)
  
  -f FORMAT, --format FORMAT
                        video file format (1=mp4v, 2=MJPG)


The default save video format is mp4v and keep the same resolution with the streaming video

# Run program

python motion_detector.py to connect with webcam

eg: python motion_detector.py --video rtsp://admin:sl888888@10.1.1.85:554 to connect with IP camera

eg: python motion_detector.py --video rtsp://admin:sl888888@10.1.1.85:554 ----area min_area 2 --format 1 to customize the sensitivity and video format

# Keyboard function:

ESC to quit the program

The video files are stored at inside the record folder
