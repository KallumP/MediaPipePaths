import cv2
import mediapipe as mp
import json

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


indexToTrack = 16
latestX = 0
latestY = 0
leniency = 0.1
points = []

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
        latestX = results.pose_landmarks.landmark[indexToTrack].x
        latestY = results.pose_landmarks.landmark[indexToTrack].y

    # progress message
    cv2.putText(image, "Points: " + str(len(points)), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # outputs the message
    cv2.imshow("Body path creating", image)

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
            with open("zBodyGesture.json", "w") as f:
                toDump = {
                    "Type": "body",
                    "Points": points
                }
                json.dump(toDump, f)
            break
        print("Empty array")

capture.release()
cv2.destroyAllWindows()
