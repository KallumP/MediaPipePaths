import cv2
import mediapipe as mp
import time
import json


def WithinTarget(index, width, height):

    filePath = "points.json"
    with open(filePath, 'r') as f:
        pointJson = json.load(f)

        toTrack = pointJson[index].get("toTrack")
        targetX = pointJson[index].get("x")
        targetY = pointJson[index].get("y")
        leniency = pointJson[index].get("leniency")

        handX = results.right_hand_landmarks.landmark[toTrack].x * width
        handY = results.right_hand_landmarks.landmark[toTrack].y * height

        xDistance2 = (targetX - handX) ** 2
        yDistance2 = (targetY - handY) ** 2

        distance = (xDistance2 + yDistance2) ** 0.5

        return distance < leniency


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

# Initializing current time and precious time for calculating the FPS
previousTime = 0
currentTime = 0
gestureIndex = 0


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
        if WithinTarget(gestureIndex, width, height):
            gestureIndex += 1

    cv2.putText(image, "Currently on: " + str(gestureIndex), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Facial and Hand Landmarks", image)

    # quit condition
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# When all the process is done
# Release the capture and destroy all windows
capture.release()
cv2.destroyAllWindows()
