import cv2
import mediapipe as mp
import json
from termcolor import colored
import math
import time
from helper import *


# opens the file
def OpenFile():
    filePath = "c:/Users/10217/Desktop/MediaPipePaths/src/DemoGesture.json"

    global pathJson
    with open(filePath, 'r') as f:
        pathJson = json.load(f)

    fileType = pathJson.get("fileType")
    return fileType == "body"

def HandleTiming(timeLimit, allPassed, keyframes):
    global keyFrameIndex
    global prevKeyFrameTime
    global gestureDetectionCount

    # checks how long since the last keyframe
    timeDifference = time.time() - prevKeyFrameTime
    if (timeLimit == -1 or timeDifference <= timeLimit):
        if allPassed:
            keyFrameIndex += 1
            prevKeyFrameTime = time.time()
            if keyFrameIndex >= len(keyframes):
                keyFrameIndex = 0
                gestureDetectionCount += 1
            return

    # if the timelimit was set and the time taken is too long
    if (timeLimit != -1 and timeDifference > timeLimit):
        keyFrameIndex = 0

    # if there is still time left (but the points were not all met)
    elif (timeLimit != -1 and timeDifference < timeLimit):
        timeLeft = round(timeLimit - timeDifference, 2)
        timeString = "Time left: " + str(timeLeft) + "s"
        cv2.putText(image, timeString, (700, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

# tracks the next keyframe of the gesture file
def TrackKeyframe(index, keyframes):
    global keyFrameIndex
    global prevKeyFrameTime
    global gestureDetectionCount

    keyframe = keyframes[index]
    points = keyframe.get("points")
    timeLimit = keyframe.get("timeLimit")

    # goes through each point in this keyframe
    allPassed = True
    for point in points:

        # gets the point type
        pointType = point.get("pointType")
        if (pointType == "triPointAngle"):
            if not WithinAngle(index, point, results.pose_landmarks.landmark):
                allPassed = False
                break
        elif (pointType == "pointPosition"):
            if not WithinTarget(keyFrameIndex, point, results.pose_landmarks.landmark):
                allPassed = False
                break
        elif (pointType == "parallelLines"):
            if not parallel(keyFrameIndex, point, results.pose_landmarks.landmark):
                allPassed = False
                break
        else:
            print(colored("Unsupported point type, point skipped", "red"))
            break

    HandleTiming(timeLimit, allPassed, keyframes)


# handles the keyboard inputs
def KeyboardInputs():
    global keyFrameIndex

    key = cv2.waitKey(2)
    if key == 27:  # esc key to quit
        print("Exit button pressed")
        return True

    elif key == 114:  # r key to restart
        keyFrameIndex = 0

    return False


if not OpenFile():
    print(colored("Bad file type", "red"))
    exit()

mp_pose = mp.solutions.pose
pose_model = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
capture = cv2.VideoCapture(0)  # video stream (the 0 implies the default camera

keyframes = pathJson.get("keyframes")
keyFrameIndex = 0
gestureDetectionCount = 0
prevKeyFrameTime = time.time()

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
        TrackKeyframe(keyFrameIndex, keyframes)


    cv2.putText(image, "Currently on index: " + str(keyFrameIndex), (10, 70),
        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(image, "Gestures detected: " + str(gestureDetectionCount), (700, 70),
        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # output image
    cv2.imshow("Body path tracking", image)

    if KeyboardInputs():
        break

capture.release()
cv2.destroyAllWindows()
