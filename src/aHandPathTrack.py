import cv2
import mediapipe as mp
import json
from termcolor import colored


def WithinTarget(index, width, height, points):

    points = pathJson.get("Points")

    point = points[index]
    toTrack = point.get("toTrack")
    targetX = point.get("x")
    targetY = point.get("y")
    leniency = point.get("leniency")

    handX = results.right_hand_landmarks.landmark[toTrack].x * width
    handY = results.right_hand_landmarks.landmark[toTrack].y * height

    xDistance2 = (targetX - handX) ** 2
    yDistance2 = (targetY - handY) ** 2

    distance = (xDistance2 + yDistance2) ** 0.5

    if distance < leniency:
        return True

    return False


# checks compatible tracking type
requiredTracking = "hands"
filePath = "gesture.json"
with open(filePath, 'r') as f:
    pathJson = json.load(f)
fileType = pathJson.get("Type")
if requiredTracking != fileType:
    print(colored("Unsupported file type", "red"))
    exit()


mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initializing the drawing utils for drawing the facial landmarks on image
mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# (0) in VideoCapture is used to connect to your computer's default camera
capture = cv2.VideoCapture(0)

gestureIndex = 0
points = pathJson.get("Points")


while capture.isOpened():

    width = 1280
    height = 720

    ret, frame = capture.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = holistic_model.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # draws the hands
    mp_drawing.draw_landmarks(
        image,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS
    )
    mp_drawing.draw_landmarks(
        image,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS
    )
    image = cv2.flip(image, 1)

    # calculates for the right hand
    if results.right_hand_landmarks:
        if WithinTarget(gestureIndex, width, height, points):
            gestureIndex += 1

    cv2.putText(image, "Currently on: " + str(gestureIndex), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Facial and Hand Landmarks", image)

    key = cv2.waitKey(2)
    if key == 27:  # esc key to quit
        break

capture.release()
cv2.destroyAllWindows()
