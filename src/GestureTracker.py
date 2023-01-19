import cv2
import mediapipe as mp
import json
from termcolor import colored
import math
import time


# Returns the distance between two points
def GetDistance(start, end):
    xDistance2 = (start[0] - end[0]) ** 2
    yDistance2 = (start[1] - end[1]) ** 2

    distance = (xDistance2 + yDistance2) ** 0.5
    return distance


# gets the angle between three points (the angle of the middle parameter)
def GetAnglePoints(trackStart, trackMid, trackEnd):
    aLength = GetDistance(trackStart, trackMid)
    bLength = GetDistance(trackMid, trackEnd)
    cLength = GetDistance(trackEnd, trackStart)

    return GetAngleLengths(aLength, bLength, cLength)


# gets the angle of three lengths using cosine rule (angle opposite length C)
def GetAngleLengths(a, b, c):
    # derivation of cosine rule
    # c^2 = a^2+b^2 - 2ab Cos(C)
    # 0 = a^2+b^2 - c^2 - 2ab Cos(C)
    # 2ab Cos(C) = a^2+b^2 - c^2
    # Cos(C) = (a^2+b^2 - c^2) / 2ab
    # C = Cos-1( (a^2+b^2 - c^2) / 2ab)

    C_rad = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
    C_deg = math.degrees(C_rad)
    return C_deg


# returns if the user's points are within the target angle
def WithinAngle(index, point):
    toTrack = point.get("toTrack")
    targetAngle = point.get("angle")
    leniency = point.get("leniency")

    # different points to track
    start = [results.pose_landmarks.landmark[toTrack[0]].x, results.pose_landmarks.landmark[toTrack[0]].y]
    mid = [results.pose_landmarks.landmark[toTrack[1]].x, results.pose_landmarks.landmark[toTrack[1]].y]
    end = [results.pose_landmarks.landmark[toTrack[2]].x, results.pose_landmarks.landmark[toTrack[2]].y]

    pointsAngle = GetAnglePoints(start, mid, end)

    # if the angle of the three points are that of the target
    if pointsAngle > targetAngle - leniency and pointsAngle < targetAngle + leniency:
        return True
    return False


# checks if a user's index is within a target position
def WithinTarget(index, point):
    toTrack = point.get("toTrack")
    leniency = point.get("leniency")
    targetPosition = [point.get("target")[0], point.get("target")[1]]

    # gets the point of the index to be tracked
    indexPosition = [results.pose_landmarks.landmark[toTrack].x, results.pose_landmarks.landmark[toTrack].y]

    distance = GetDistance(indexPosition, targetPosition)

    if distance < leniency:
        return True
    return False


# Deals with tracking the next keyframe of the gesture file
def TrackKeyframe(index, keyframes):
    global keyFrameIndex
    global prevKeyFrameTime
    global finished

    keyframe = keyframes[index]
    points = keyframe.get("points")
    timeLimit = keyframe.get("timeLimit")

    # goes through each point in this keyframe
    allPassed = True
    for point in points:

        # gets the point type
        pointType = point.get("pointType")
        if (pointType == "triPointAngle"):
            if not WithinAngle(index, point):
                allPassed = False
                break
        elif (pointType == "pointPosition"):
            if not WithinTarget(keyFrameIndex, point):
                allPassed = False
                break
        else:
            print(colored("Unsupported point type, point skipped", "red"))
            break

    # checks how long since the last keyframe
    timeDifference = time.time() - prevKeyFrameTime
    if (timeLimit == -1 or timeDifference <= timeLimit):
        if allPassed:
            keyFrameIndex += 1
            prevKeyFrameTime = time.time()
            finished = keyFrameIndex >= len(keyframes)
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


mp_pose = mp.solutions.pose
pose_model = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
capture = cv2.VideoCapture(0) # video stream (the 0 implies the default camera

filePath = "DemoGesture.json"
with open(filePath, 'r') as f:
    pathJson = json.load(f)
keyframes = pathJson.get("keyframes")
keyFrameIndex = 0
finished = False
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
    if results.pose_landmarks and not finished:
        TrackKeyframe(keyFrameIndex, keyframes)

    # progress message
    if (finished):
        cv2.putText(image, "Finished", (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(image, "Currently on: " + str(keyFrameIndex), (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # output image
    cv2.imshow("Body path tracking", image)

    key = cv2.waitKey(2)
    if key == 27:  # esc key to quit
        break

    elif key == 114:  # r key to restart
        keyFrameIndex = 0
        finished = False

capture.release()
cv2.destroyAllWindows()
