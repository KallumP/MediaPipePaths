import cv2
import mediapipe as mp
import json


mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# (0) in VideoCapture is used to connect to your computer's default camera
capture = cv2.VideoCapture(0)


indexToTrack = 0
latestX = 0
latestY = 0
leniency = 100
points = []

while capture.isOpened():

    width = 1280
    height = 720

    # processes this frame
    ret, frame = capture.read()
    frame = cv2.resize(frame, (width, height))
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

    # progress message
    cv2.putText(image, "Points: " + str(len(points)), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # output image
    cv2.imshow("Hand path creating", image)

    key = cv2.waitKey(2)
    if key == 27:  # esc key to quit
        break

    elif key == 32:  # space to ad a new point
        points.append({
            "toTrack": indexToTrack,
            "x": latestX,
            "y": latestY,
            "leniency": leniency
        })

    elif key == 13:  # enter to finish gesture
        print("Finish button pressed")
        if (points != []):
            with open("zHandGesture.json", "w") as f:
                toDump = {
                    "Type": "hands",
                    "Points": points
                }
                json.dump(toDump, f)
            break
        print("Empty array")

capture.release()
cv2.destroyAllWindows()
