import cv2
import mediapipe as mp
import json
from termcolor import colored


def WithinTarget(index, width, height, points):

    point = points[index]
    toTrack = point.get("toTrack")
    targetX = point.get("x")
    targetY = point.get("y")
    leniency = point.get("leniency")

    handX = results.pose_landmarks.landmark[toTrack].x
    handY = results.pose_landmarks.landmark[toTrack].y

    xDistance2 = (targetX - handX) ** 2
    yDistance2 = (targetY - handY) ** 2

    distance = (xDistance2 + yDistance2) ** 0.5

    if distance < leniency:
        return True

    return False


# checks compatible tracking type
requiredTracking = "body"
filePath = "zBodyGesture.json"
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
print(len(points))

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

        # checks if the point to track was within the current path keyframe
        if WithinTarget(gestureIndex, width, height, points):
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
