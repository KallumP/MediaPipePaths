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
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import os
import os.path
from os import listdir
from os.path import isfile, join
import json

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class NewExercise(Screen):
    def __init__(self, **kwargs):
        super(NewExercise, self).__init__(**kwargs) 
        self.layout = FloatLayout()

        input_area = BoxLayout(orientation = 'vertical', size_hint = (0.5, 0.5), pos_hint = {'center_y': 0.6, 'center_x': 0.5})

        input_area.add_widget(Label(text='Add new exercise', font_size='30sp'))

        input_area.add_widget(Label(text='Exercise name', font_size='20sp',size_hint=(1, 0.2)))

        self.exercise_name = TextInput(text = '', font_size = '25sp', size_hint = (1, 0.3), multiline = False)
        input_area.add_widget(self.exercise_name)

        input_area.add_widget(Label(text='Exercise video link', font_size='20sp',size_hint=(1, 0.2)))

        self.exercise_video_link = TextInput(text = '', font_size = '25sp', size_hint = (1, 0.3), multiline = False)
        input_area.add_widget(self.exercise_video_link)

        self.layout.add_widget(input_area)
        
        add_exercise_btn = Button(text="New exercise",size_hint=(0.5, 0.08),pos_hint={'center_y': 0.2, 'center_x': 0.5})
        add_exercise_btn.bind(on_press=self.create_exercise)
        self.layout.add_widget(add_exercise_btn)

        cancel_btn = Button(text="Cancel",size_hint=(0.5, 0.08),pos_hint={'center_y': 0.1, 'center_x': 0.5})
        cancel_btn.bind(on_press=self.cancel)
        self.layout.add_widget(cancel_btn)

        self.add_widget(self.layout)

    def create_exercise(self, instance):
        self.manager.get_screen('edit exercise').exercise_name = str(self.exercise_name.text)
        self.manager.get_screen('edit exercise').exercise_video_link = str(self.exercise_video_link.text)
        self.manager.current = 'edit exercise'
        self.manager.get_screen('edit exercise').refresh()

    def cancel(self, instance):
        self.manager.current = 'home'