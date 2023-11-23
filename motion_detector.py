# USAGE
# python motion_detector.py
# or
# python motion_detector.py --video rtsp://admin:sl888888@10.1.1.85:554
# or
# python motion_detector.py --video video_path --area min_area --format 1 

# import the necessary packages
import argparse
import datetime
import imutils
import time
import shutil
import cv2
import os

Keep_Data = 30 #keep 30 days record
Display_Resolution = (800, 600)
Video_Resolution = (500, 312)
Video_FPS = 20
Motion_Start = True
Motion_End = False
Newline_Log = False
Motion_Refresh = 0
CurrentDate = datetime.datetime.now()
Refresh_Time = CurrentDate.strftime("%H;%M;%S")
FolderDate = CurrentDate.strftime("%Y-%m-%d")
File_Name = "./record/" + FolderDate + "/" + CurrentDate.strftime("%Y-%m-%d") + ".csv"
Video_NewDate = CurrentDate.strftime("%Y-%m-%d")
out = None
previous_frame = None
text = ""
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

def Delete_Old_Record(day):
    today = datetime.datetime.today()
    days_ago = today - datetime.timedelta(days=Keep_Data)
    print(days_ago)
    while(True):
        for x in range(int(day)):
            try:
                day_ago = days_ago - datetime.timedelta(days=x) 
                video_name = day_ago.strftime("%Y-%m-%d")
                print("Delete ", video_name)
                shutil.rmtree("./record/" + video_name)
            except:
                print("No video")
                continue
        break

def Create_File():
    global File_Name
    CurrentDate = datetime.datetime.now()
    FolderDate = "./record/" +CurrentDate.strftime("%Y-%m-%d")
    if not os.path.exists(FolderDate): os.makedirs(FolderDate)
    File_Name = FolderDate + "/" + CurrentDate.strftime("%Y-%m-%d") + ".csv"
    if os.path.exists(File_Name): flag_file = True
    else:
        print("The file does not exist")
        f = open(File_Name, "a")
        f.write("              Start, End")
        f.write("\n")
        f.close()
        flag_file = False
    return flag_file

def Create_VideoFile():
    global Video_NewDate, out
    CurrentDate = datetime.datetime.now()
    FolderDate = "./record/" + CurrentDate.strftime("%Y-%m-%d")
    if not os.path.exists(FolderDate): os.makedirs(FolderDate)
    if out is None or out.isOpened() is False:
        Video_Name = FolderDate + "/" + CurrentDate.strftime("%Y-%m-%d_%H;%M;%S") + ".avi" 
        out = cv2.VideoWriter(Video_Name, fourcc, Video_FPS, Video_Resolution) 
        print("Start video file")
    else:
        Video_CurrentDate = CurrentDate.strftime("%Y-%m-%d")
        if Video_NewDate != Video_CurrentDate:
            Video_NewDate = Video_CurrentDate
            Delete_Old_Record(1)
            Video_Name = FolderDate + "/" + Video_CurrentDate + ".avi"
            print(Video_Name)
            if out.isOpened() is True:
                out.release()
                out = cv2.VideoWriter(Video_Name, fourcc, Video_FPS, Video_Resolution) 
                print("New video file")

def motion_detect(frame, previous_frame, motion_area=1000):
    motion = False
    if frame is not None and previous_frame is not None:
        (h1, w1) = frame.shape[:2]
        (h2, w2) = previous_frame.shape[:2]
        if h1 == h2 and w1 == w2:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
            previous_gray = cv2.GaussianBlur(previous_gray, (21, 21), 0)
            frame_delta = cv2.absdiff(previous_gray, gray)
            thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1] #less than 30 to black
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < motion_area: continue
                motion = True
                break
            #cv2.imshow("frame_delta", frame_delta)
            #cv2.waitKey(1)
    return motion

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(description="motion_detector")
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--area", type=int, default=800, help="minimum area size (default=800)")
ap.add_argument("-f", "--format", type=int, default=1, help="video file format (1=mp4v, 2=MJPG)")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    #vs = cv2.VideoCapture("./example_02.mp4")
    #vs = cv2.VideoCapture("rtsp://admin:sl888888@192.168.2.86") # ip camera
    vs = cv2.VideoCapture(0)
    print(vs.get(cv2.CAP_PROP_FRAME_WIDTH), vs.get(cv2.CAP_PROP_FRAME_HEIGHT), 
          vs.get(cv2.CAP_PROP_FPS), vs.get(cv2.CAP_PROP_FRAME_COUNT))
# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])
    print(vs.get(cv2.CAP_PROP_FRAME_WIDTH), vs.get(cv2.CAP_PROP_FRAME_HEIGHT), vs.get(cv2.CAP_PROP_FPS))

if args["format"] == 1: fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
elif args["format"] == 2: fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

Delete_Old_Record(60)
time.sleep(2.0)
ret, frame = vs.read()
if ret is True:
    Video_Resolution = (frame.shape[1], frame.shape[0])
    print(Video_Resolution)

    if out is None: pass
    elif out.isOpened() is True: out.release()

while(ret):
    # grab the current frame and initialize the motion detection
    ret, frame = vs.read()
    if ret is False:
        break

    live_frame = frame.copy()
    display_frame = frame.copy()
    # if the previous frame is None, initialize it
    if previous_frame is None:
        previous_frame = frame.copy()
        #cv2.imshow("previous_frame", previous_frame)
        #cv2.waitKey(1)
        continue
    elif Motion_Refresh >= 60:
        Motion_Refresh = 0
        previous_frame = frame.copy()
        #cv2.imshow("previous_frame", previous_frame)
        #cv2.waitKey(1)
    # check motion
    if motion_detect(frame, previous_frame, motion_area=args["area"]):
        text = "Motion"
        Current_Time = datetime.datetime.now().strftime("%H;%M;%S")
        if Refresh_Time != Current_Time:
            Refresh_Time = Current_Time
            Motion_Refresh += 1
        if Motion_Start is True:
            Create_File()
            f = open(File_Name, "a")
            f.write(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S, "))
            f.close()
            Motion_Start = False
            Motion_End = True
            Newline_Log = False
            # initialize the next frame in the video stream
            Create_VideoFile()
        cv2.putText(live_frame, datetime.datetime.now().strftime("%A %d %B %Y %H:%M:%S%p"),
            (10, live_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, Video_Resolution[0]/1500, (0, 0, 255), 1)
        if out is None: pass
        elif out.isOpened() is True: out.write(live_frame) # save the motion video
    else:
        text = ""
        if Motion_End is True:
            Create_File()
            f = open(File_Name, "a")
            f.write(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
            f.write("\n")
            f.close()
            Motion_Start = True
            Motion_End = False
            Newline_Log = True
        Motion_Refresh = 0

    cv2.putText(display_frame, datetime.datetime.now().strftime("%A %d %B %Y %H:%M:%S%p"),
        (10, live_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, Video_Resolution[0]/1500, (0, 0, 255), 1)
    cv2.putText(display_frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, Video_Resolution[0]/1000, (0, 0, 255), 2)
    display_frame = cv2.resize(display_frame, Display_Resolution, interpolation=cv2.INTER_AREA)
    cv2.imshow("Security Live Feed", display_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27: #esc key to exit
        break

# cleanup the camera and close any open windows
if Newline_Log is False:
    if Create_File() is True:
        f = open(File_Name, "a")
        f.write("\n")
        f.close()
        Newline_Log = True
if out is None: pass
elif out.isOpened() is True: out.release()
vs.release()
cv2.destroyAllWindows()
print("End")
