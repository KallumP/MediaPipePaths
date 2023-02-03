from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2

import mediapipe as mp
import json
from termcolor import colored
import math
import time

class AdminApp(App):

    def build(self):
        self.img1=Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        record_btn = Button(text='Record frame',size_hint=(0.1, 0.1),pos_hint={'center_y': 0.8, 'center_x': 0.5})
        record_btn.bind(on_press=self.recordFrame)
        layout.add_widget(record_btn)
        #mediaPipe
        self.mp_pose = mp.solutions.pose
        self.pose_model = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        #cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/3000.0)
        return layout

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        frame = cv2.resize(frame, (1280, 720))
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
        # convert it to texture
        buf1 = cv2.flip(image, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')  
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

    def recordFrame(self, instance):
        print(self.results.pose_landmarks)

if __name__ == '__main__':
    AdminApp().run()
    cv2.destroyAllWindows()