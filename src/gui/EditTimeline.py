from imp import reload
from re import L, template
import re
from turtle import onclick
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

import os
import os.path
from os import listdir
from os.path import isfile, join
import json

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class EditTimeline(Screen):
    def __init__(self, **kwargs):
        super(EditTimeline, self).__init__(**kwargs) 
        self.layout = FloatLayout()

        self.timeline_layout = BoxLayout(orientation='vertical',size_hint=(1, 0.7),pos_hint={'center_y': 0.5, 'center_x': 0.5})
        self.layout.add_widget(self.timeline_layout)

        new_exercise_btn = Button(text="Add new exercise",size_hint=(1, 0.05),pos_hint={'center_y': 0.8, 'center_x': 0.5})
        new_exercise_btn.bind(on_press=self.create_exercise)
        self.layout.add_widget(new_exercise_btn)

        cancel_btn = Button(text="Cancel",size_hint=(1, 0.05))
        cancel_btn.bind(on_press=self.cancel)
        self.layout.add_widget(cancel_btn)

        self.add_widget(self.layout)

    def create_exercise(self, instance):
        self.manager.current = 'new exercise'

    def cancel(self, instance):
        os.chdir('..')
        os.chdir('..')
        self.manager.current = 'home'


    def update_timeline(self, instance):
        self.instance.text
        f = open("TimelineList.json", "w")
        TimelineListStart = """{\n    "fileType": "timeline",\n    "timeline": [\n    """        
        f.write(TimelineListStart)

        #Write exercise here

        TimelineListEnd = """]\n}"""  
        f.write(TimelineListEnd) 
        f.close()  
