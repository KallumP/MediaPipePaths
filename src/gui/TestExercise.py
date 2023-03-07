import cv2
import mediapipe as mp
import json
from termcolor import colored
import math
import time
from src.helper import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import cv2
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import mediapipe as mp
from kivy.clock import Clock
import cv2
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

testing = False
testing_exercise_json = ""


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class TestExercise(Screen):
    def __init__(self, **kwargs):
        super(TestExercise, self).__init__(**kwargs) 
        self.layout = BoxLayout(orientation = 'vertical')

        self.texture1 = None

        # this area is used to show gestures catched by camera
        image_area = BoxLayout(size_hint=(1, 0.9))
        self.img1 = Image()
        image_area.add_widget(self.img1)
        #mediaPipe
        self.mp_pose = mp.solutions.pose
        self.pose_model = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        #self.update_event = Clock.schedule_interval(self.update, 1.0/3000.0)
        self.update_event = None

        self.layout.add_widget(image_area)

        btn_area = BoxLayout(orientation = 'vertical', size_hint=(1, 0.05))

        self.cancel_btn = Button(text="Return",size_hint=(1, 0.1), pos_hint={'center_x': 0.5}, disabled = False)
        self.cancel_btn.bind(on_press=self.cancel)
        btn_area.add_widget(self.cancel_btn)        

        self.layout.add_widget(btn_area)
        self.add_widget(self.layout)

    def start_update(self):
        self.prevKeyFrameTime = time.time()
        self.keyFrameIndex = 0
        self.gestureDetectionCount = 0
        self.OpenFile()
        self.keyframes = self.pathJson.get("keyframes")
        self.update_event = Clock.schedule_interval(self.update, 1.0/3000.0)

    def cancel(self, instance):
        if self.update_event is not None and self.update_event.is_triggered:
            self.update_event.cancel()
        self.manager.current = 'edit timeline'

    def update(self, instance):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        #frame = cv2.resize(frame, (1280, 720))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        self.results = self.pose_model.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # draws the body
        self.mp_drawing.draw_landmarks(
            image,
            self.results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        image = cv2.flip(image, 1)

        if testing == True:
            self.testing_exercise(image)
        else:
            cv2.putText(image, "Exercise complete", (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)   

        # convert it to texture
        buf1 = cv2.flip(image, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')  
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1             
    
    def testing_exercise(self, image):
        # if there were results to process
        if self.results.pose_landmarks:
            self.TrackKeyframe(self.keyFrameIndex, self.keyframes, image)
        cv2.putText(image, "Currently on index: " + str(self.keyFrameIndex), (10, 70),
            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # tracks the next keyframe of the gesture file
    def TrackKeyframe(self,index, keyframes, image):
        #print(self.results.pose_landmarks.landmark)

        self.keyframe = keyframes[index]
        points = self.keyframe.get("points")
        timeLimit = self.keyframe.get("timeLimit")

        # goes through each point in this keyframe
        allPassed = True
        for point in points:
        
            # gets the point type
            pointType = point.get("pointType")
            if (pointType == "triPointAngle"):
                if not WithinAngle(point, self.results.pose_landmarks.landmark):
                    allPassed = False
                    break
            elif (pointType == "pointPosition"):
                #change from within to above
                if not WithinTarget(point, self.results.pose_landmarks.landmark):
                    allPassed = False
                    break
            elif (pointType == "parallelLines"):
                if not parallel(point, self.results.pose_landmarks.landmark):
                    allPassed = False
                    break
            elif (pointType == "abovePosition"):
                #change from within to above
                if not AboveTarget(point, self.results.pose_landmarks.landmark):
                    allPassed = False
                    break
            else:
                print(colored("Unsupported point type, point skipped", "red"))
                break

        self.HandleTiming(timeLimit, allPassed, keyframes, image)

    # opens the file
    def OpenFile(self):
        filePath = testing_exercise_json

        self.pathJson = None
        with open(filePath, 'r') as f:
            self.pathJson = json.load(f)

        #fileType = self.pathJson.get("fileType")
        #return fileType == "body"

    def HandleTiming(self, timeLimit, allPassed, keyframes, image):
        global testing
        # checks how long since the last keyframe
        timeDifference = time.time() - self.prevKeyFrameTime
        if (timeLimit == -1 or timeDifference <= timeLimit):
            if allPassed:
                self.keyFrameIndex += 1
                self.prevKeyFrameTime = time.time()
                if self.keyFrameIndex >= len(keyframes):
                    #self.keyFrameIndex = 0
                    testing = False              
                    #self.update_event.cancel()
                    self.gestureDetectionCount += 1
                return

        # if the timelimit was set and the time taken is too long
        if (timeLimit != -1 and timeDifference > timeLimit):
            self.keyFrameIndex = 0

        # if there is still time left (but the points were not all met)
        elif (timeLimit != -1 and timeDifference < timeLimit):
            timeLeft = round(timeLimit - timeDifference, 2)
            timeString = "Time left: " + str(timeLeft) + "s"
            cv2.putText(self.test_image, timeString, (700, 70),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    

    
