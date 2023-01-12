import cv2
import mediapipe as mp
import time
import json


def WithinTarget(index, xPoint, yPoint, json):

    filePath = "points.json"
    with open(filePath, 'w') as f:
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

        testLinks.append({
            "testFile": testFile,
            "testFileDate": str(testDate),
            "testFileSize": testSize,
            "testedFile": testedFile,
            "testedFileDate": str(testedDate),
            "testdFileSize": testedSize
        })


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

indexToTrack = 0
latestX = 0
latestY = 0
leniency = 100
points = []

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
        latestX = results.right_hand_landmarks.landmark[indexToTrack].x * width
        latestY = results.right_hand_landmarks.landmark[indexToTrack].y * height

    cv2.putText(image, "Points: " + str(len(points)), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Facial and Hand Landmarks", image)

    key = cv2.waitKey(2)
    if key == 27:  # esc key to quit
        break

    # add point condition
    elif key == 32:
        points.append({
            "toTrack": indexToTrack,
            "x": latestX,
            "y": latestY,
            "leniency": leniency
        })

    # finish path condition
    elif key == 13:
        print("Finish button pressed")
        if (points != []):
            with open("gesture.json", "w") as f:
                json.dump(points, f)
            break
        print("Empty array")
        # When all the process is done
        # Release the capture and destroy all windows
capture.release()
cv2.destroyAllWindows()
