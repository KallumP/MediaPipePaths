from imp import reload
from re import L, template
import re
import mediapipe as mp
from kivy.clock import Clock
import cv2
from kivy.graphics.texture import Texture
from turtle import onclick
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import os
from kivy.uix.image import Image
import os.path
from os import listdir
from os.path import isfile, join
import json

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class EditExercise(Screen):
    def __init__(self, **kwargs):

        super(EditExercise, self).__init__(**kwargs) 

        self.exercise_name = ""
        self.exercise_video_link = ""
        self.frame_index = 0
        
        self.layout = FloatLayout()

        # info area contains information about frame name and frame index
        info_area = BoxLayout(orientation = 'horizontal', size_hint = (0.9, 0.5), pos_hint = {'center_y': 0.8, 'center_x': 0.5})
        name_box = BoxLayout(size_hint = (0.5, 0.5), pos_hint = {'center_y': 0.8, 'center_x': 0})
        self.name_label = Label(text=self.exercise_name, font_size='30sp')
        name_box.add_widget(self.name_label)
        info_area.add_widget(name_box)
        frame_box = BoxLayout(size_hint = (0.5, 0.5), pos_hint = {'center_y': 0.8, 'center_x': 0.5})
        self.frame_label = Label(text='Current frame:' + str(self.frame_index), font_size='30sp')
        frame_box.add_widget(self.frame_label)
        info_area.add_widget(frame_box)
        self.layout.add_widget(info_area)

        # edit box contains two area: frame area(left) and edit area(right)
        edit_box = BoxLayout(orientation = 'horizontal', size_hint = (0.9, 0.5), pos_hint = {'center_y': 0.6, 'center_x': 0.5})

        # frame area is used to record frame
        frame_area = BoxLayout(orientation = 'vertical', size_hint = (0.5, 1), pos_hint = {'center_y': 0.6, 'center_x': 0.5})
        frame_area.add_widget(Label(text='Recorded frame', font_size='30sp'))

        # this area is used to show gestures catched by camera
        image_area = BoxLayout()
        self.img1=Image()
        image_area.add_widget(self.img1)
        frame_area.add_widget(image_area)
        #mediaPipe
        self.mp_pose = mp.solutions.pose
        self.pose_model = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/3000.0)

        record_frame_btn = Button(text="Record frame",size_hint=(0.5, 0.05),pos_hint={'center_x': 0.5})
        record_frame_btn.bind(on_press=self.record_frame)
        frame_area.add_widget(record_frame_btn)

        edit_box.add_widget(frame_area)

        # edit area is used to edit exercise, like selecting points and indexes
        edit_area = BoxLayout(orientation = 'vertical', size_hint = (0.5, 1), pos_hint = {'center_y': 0.6, 'center_x': 0.5})
        edit_area.add_widget(Label(text='Select target index', font_size='30sp'))
        edit_area.add_widget(Label(text='Set leniency', font_size='30sp'))

        btn_box = BoxLayout(orientation = 'horizontal', size_hint = (0.8, 0.4), pos_hint = {'center_x': 0.5})

        reset_btn = Button(text="Reset exercise",size_hint=(0.2, 0.05))
        reset_btn.bind(on_press=self.reset)

        next_btn = Button(text="Next frame",size_hint=(0.2, 0.05), pos_hint = {'center_x': 0.5})
        next_btn.bind(on_press=self.next)

        complete_btn = Button(text="Complete exercise",size_hint=(0.2, 0.05))
        complete_btn.bind(on_press=self.complete)

        btn_box.add_widget(reset_btn)
        btn_box.add_widget(next_btn)
        btn_box.add_widget(complete_btn)
        edit_area.add_widget(btn_box)
        edit_box.add_widget(edit_area)

        self.layout.add_widget(edit_box)

        cancel_btn = Button(text="Cancel",size_hint=(1, 0.05))
        cancel_btn.bind(on_press=self.cancel)
        self.layout.add_widget(cancel_btn)


        self.add_widget(self.layout)

    def record_frame(self, instance):
        print(self.results.pose_landmarks)
    
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

    def reset(self, instance):
        return 1
    
    def next(self, instance):
        return 1

    def complete(self, instance):
        return 1

    def cancel(self, instance):
        self.manager.current = 'home'
    
    def refresh(self):
        self.name_label.text = self.exercise_name