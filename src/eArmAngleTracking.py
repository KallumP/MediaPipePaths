import cv2
import mediapipe as mp
import json
from termcolor import colored
import math
import time

gestureIndex = 0

def GetDistance(start, end):

    xDistance2 = (start[0] - end[0]) ** 2
    yDistance2 = (start[1] - end[1]) ** 2

    distance = (xDistance2 + yDistance2) ** 0.5
    return distance


def GetAnglePoints(trackStart, trackMid, trackEnd):

    aLength = GetDistance(trackStart, trackMid)
    bLength = GetDistance(trackMid, trackEnd)
    cLength = GetDistance(trackEnd, trackStart)

    return GetAngleLengths(aLength, bLength, cLength)


def GetAngleLengths(a, b, c):

    # derivation of cosine rule
    # c^2 = a^2+b^2 - 2ab Cos(C)
    # 0 = a^2+b^2 - c^2 - 2ab Cos(C)
    # 2ab Cos(C) = a^2+b^2 - c^2
    # Cos(C) = (a^2+b^2 - c^2) / 2ab
    # C = Cos-1( (a^2+b^2 - c^2) / 2ab)

    C_rad = math.acos((a**2 + b**2 - c**2) / (2*a*b))
    C_deg = math.degrees(C_rad)
    return C_deg


def WithinAngle(index, points):

    point = points[index]
    toTrack = point.get("toTrack")
    targetAngle = point.get("angle")
    leniency = point.get("leniency")
    timeLimit = point.get("timeLimit")
    
    #checks how long since 
    timeDifference = time.time() - prevGestureTime 
    if (timeLimit == -1 or timeDifference <= timeLimit):

        #different points to track
        start = [results.pose_landmarks.landmark[toTrack[0]].x,
                results.pose_landmarks.landmark[toTrack[0]].y]

        mid = [results.pose_landmarks.landmark[toTrack[1]].x,
                results.pose_landmarks.landmark[toTrack[1]].y]

        end = [results.pose_landmarks.landmark[toTrack[2]].x,
                results.pose_landmarks.landmark[toTrack[2]].y]

        elbowAngle = GetAnglePoints(start, mid, end)

        #if the angle of the three points are that of the target
        if elbowAngle > targetAngle - leniency and elbowAngle < targetAngle + leniency:
            return True   
    
    #if the timelimit was set and the time taken is too long
    if (timeLimit != -1 and timeDifference > timeLimit):
        global gestureIndex
        gestureIndex = 0
        
    elif (timeLimit != -1 and timeDifference < timeLimit):
        
        timeLeft = round(timeLimit - timeDifference, 2)
        timeString = "Time left: " + str(timeLeft) + "s"
        #outputs the time left
        cv2.putText(image, timeString, (700, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    return False      


# checks compatible tracking type
requiredTracking = "bodyAngles"
filePath = "zPunchingGesture.json"
with open(filePath, 'r') as f:
    pathJson = json.load(f)
fileType = pathJson.get("Type")
if requiredTracking != fileType:
    print(colored("Unsupported file type", "red"))
    exit()

mp_pose = mp.solutions.pose
pose_model = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Initializing the drawing utils for drawing the facial landmarks on image
mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# (0) in VideoCapture is used to connect to your computer's default camera
capture = cv2.VideoCapture(0)

finished = False
points = pathJson.get("Points")
prevGestureTime = time.time()

while capture.isOpened():

    width = 1280
    height = 720
    # width = 1920
    # height = 1080

    # processes this frame
    ret, frame = capture.read()
    frame = cv2.resize(frame, (width, height))
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose_model.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # draws the body
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    image = cv2.flip(image, 1)

    # if there were results to process
    if results.pose_landmarks and not finished:

        if WithinAngle(gestureIndex, points):
            gestureIndex += 1
            finished = gestureIndex >= len(points)
            prevGestureTime = time.time()

    # progress message
    if (finished):
        cv2.putText(image, "Finished", (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(image, "Currently on: " + str(gestureIndex), (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # output image
    cv2.imshow("Body path tracking", image)

    key = cv2.waitKey(2)
    if key == 27:  # esc key to quit
        break

    elif key == 114:  # r key to restart
        gestureIndex = 0
        finished = False

capture.release()
cv2.destroyAllWindows()
