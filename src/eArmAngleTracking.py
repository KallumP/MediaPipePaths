import cv2
import mediapipe as mp
import json
from termcolor import colored
import math


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

    # derivation
    # c^2 = a^2+b^2 - 2ab Cos(C)
    # 0 = a^2+b^2 - c^2 - 2ab Cos(C)
    # 2ab Cos(C) = a^2+b^2 - c^2
    # Cos(C) = (a^2+b^2 - c^2) / 2ab
    # C = Cos-1( (a^2+b^2 - c^2) / 2ab)

    C_rad = math.acos((a*a + b*b - c*c) / (2*a*b))
    C_deg = math.degrees(C_rad)
    return C_deg


def WithinAngle(index, points):

    point = points[index]
    toTrack = point.get("toTrack")
    targetAngle = point.get("angle")
    leniency = point.get("leniency")

    shoulder = [results.pose_landmarks.landmark[toTrack[0]].x,
                results.pose_landmarks.landmark[toTrack[0]].y]

    elbow = [results.pose_landmarks.landmark[toTrack[1]].x,
             results.pose_landmarks.landmark[toTrack[1]].y]

    wrist = [results.pose_landmarks.landmark[toTrack[2]].x,
             results.pose_landmarks.landmark[toTrack[2]].y]

    elbowAngle = GetAnglePoints(shoulder, elbow, wrist)
    # return elbowAngle

    if elbowAngle > targetAngle - leniency and elbowAngle < targetAngle + leniency:
        return True


# checks compatible tracking type
requiredTracking = "bodyAngles"
filePath = "zBodyGestureAngle.json"
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
gestureIndex = 0
points = pathJson.get("Points")


trackStart = 16
trackMid = 14
trackEnd = 12
lastAngle = -1

while capture.isOpened():

    width = 1280
    height = 720

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
