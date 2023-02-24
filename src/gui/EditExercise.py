import mediapipe as mp
from kivy.clock import Clock
import cv2
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
import json
from kivy.graphics import Ellipse, Color, Line

import src.helper

key_frame_index_result = []

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
        self.img1=Image(size=(400, 400), allow_stretch=True, keep_ratio=True)
        image_area.add_widget(self.img1)
        frame_area.add_widget(image_area)

        record_frame_btn = Button(text="Record frame",size_hint=(0.5, 0.05),pos_hint={'center_x': 0.5})
        record_frame_btn.bind(on_press=self.record_frame)
        frame_area.add_widget(record_frame_btn)

        edit_box.add_widget(frame_area)

        # edit area is used to edit exercise, like selecting points and indexes
        edit_area = BoxLayout(orientation = 'vertical', size_hint = (0.5, 1), pos_hint = {'center_y': 0.6, 'center_x': 0.5})
        edit_area.add_widget(Label(text='Select target index', font_size='30sp'))

        # # select area is used to select indexes
        select_area = FloatLayout()
        with select_area.canvas:
            Color(1, 1, 1)  # set color to white
            Line(circle=(select_area.width/2, select_area.height/2, min(select_area.width, select_area.height)/2), width=2)  # draw a border around the circle
            Ellipse(pos=(select_area.width/2 - min(select_area.width, select_area.height)/2, 
            select_area.height/2 - min(select_area.width, select_area.height)/2), 
            size=(min(select_area.width, select_area.height), min(select_area.width, select_area.height)), 
            angle_end=360)  # draw an empty circle

        edit_area.add_widget(select_area)

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
        self.manager.current = 'record frame'
        
    def reset(self, instance):
        return 1
    
    def next(self, instance):
        return 1

    def complete(self, instance):
        global key_frame_index_result

        target_index = [{12,14,16}]

        print(key_frame_index_result)

        src.helper.CheckWithinFrame(target_index)
        return 1

    def cancel(self, instance):
        self.manager.current = 'home'
    
    def refresh(self):
        self.name_label.text = self.exercise_name

    def update_exercise_json(self):
        
        with open(self.name_label.text + ".json",'r+') as file:
          # First we load existing data into a dict.
            exercise_data = json.load(file)
            
            # python object to be appended
            #new_keyframe = {"exercise": self.exercise_name.text+".json"}
            
            # appending the data
            #timeline_data["keyframes"].append(new_keyframe)
            
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(exercise_data, file, indent = 4)