import cv2
import mediapipe as mp
import json
from termcolor import colored
import math
import time
from helper import *

import cv2
import mediapipe as mp
import json


def AddPointsToKeyframes(points):
    global keyframes
    keyFrame = {
        "points": points,
        "timeLimit": -1
    }
    keyframes.append(keyFrame)


def GetBodyMetrics(results):
    global lastPosition
    lastPosition = [results[toTrackPosition[0]].x, results[toTrackPosition[0]].y]

    global lastAngle
    lastAngle = GetAnglePoints(
        [results[toTrackAngle[0]].x, results[toTrackAngle[0]].y],
        [results[toTrackAngle[1]].x, results[toTrackAngle[1]].y],
        [results[toTrackAngle[2]].x, results[toTrackAngle[2]].y])


def KeyboardInputs():

    key = cv2.waitKey(2)

    if key == 27:  # esc key to quit
        print("Exit button pressed")
        return True

    elif key == 112:  # p key to add a new point
        print("New point added")
        points = [{
            "pointType": "pointPosition",
            "toTrack": toTrackPosition,
            "target": lastPosition,
            "leniency": pointLeniency
        }]
        AddPointsToKeyframes(points)

    elif key == 97:  # a key to add a new angle
        print("New angle added")
        points = [{
            "pointType": "triPointAngle",
            "toTrack": toTrackAngle,
            "angle": lastAngle,
            "leniency": angleLeniency
        }]
        AddPointsToKeyframes(points)

    elif key == 13:  # enter to finish gesture
        print("Finish button pressed")
        if (keyframes != []):
            with open("zBodyGesture.json", "w") as f:
                toDump = {
                    "fileType": "body",
                    "keyframes": keyframes
                }
                json.dump(toDump, f)
        else:
            print("Empty array")
        return True

    return False


mp_pose = mp.solutions.pose
pose_model = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
capture = cv2.VideoCapture(0)  # video stream (the 0 implies the default camera

keyframes = []

# pointPosition
toTrackPosition = [16]
lastPosition = [0, 0]
pointLeniency = 0.1

# triPointAngle
toTrackAngle = [16, 14, 12]
lastAngle = 0
angleLeniency = 20

# runs while the
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
    if results.pose_landmarks:
        GetBodyMetrics(results.pose_landmarks.landmark)

    # progress message
    cv2.putText(image, "Points: " + str(len(keyframes)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # outputs the message
    cv2.imshow("Gesture editor", image)

    if KeyboardInputs():
        break

capture.release()
cv2.destroyAllWindows()
