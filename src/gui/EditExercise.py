from imp import reload
from re import L, template
import re
from turtle import onclick
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
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

class EditExercise(Screen):
    def __init__(self, **kwargs):
        super(EditExercise, self).__init__(**kwargs) 
        self.layout = FloatLayout()

        record_frame_btn = Button(text="Record frame exercise",size_hint=(1, 0.05),pos_hint={'center_y': 0.5, 'center_x': 0.5})
        record_frame_btn.bind(on_press=self.record_frame)
        self.layout.add_widget(record_frame_btn)

        cancel_btn = Button(text="Cancel",size_hint=(1, 0.05))
        cancel_btn.bind(on_press=self.cancel)
        self.layout.add_widget(cancel_btn)

        self.add_widget(self.layout)

    def record_frame(self, instance):
        self.manager.current = 'record frame'

    def cancel(self, instance):
        self.manager.current = 'edit timeline'