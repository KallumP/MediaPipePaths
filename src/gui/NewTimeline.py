from imp import reload
from re import L, template
import re
from turtle import onclick
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


import os.path
from os import path

import os
import errno

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class NewTimeline(Screen): 
    def __init__(self, **kwargs):
        super(NewTimeline, self).__init__(**kwargs)
        layout = FloatLayout()

        input_area = BoxLayout(orientation = 'vertical',size_hint=(0.5, 0.5),pos_hint={'center_y': 0.5, 'center_x': 0.5})
        input_area.add_widget(Label(text='Enter timeline name', font_size='30sp',size_hint=(1, 0.2)))

        self.timeline_name = TextInput(text='', font_size='25sp',size_hint=(1, 0.05), multiline=False)
        input_area.add_widget(self.timeline_name)

        self.warning_message = Label(text='', font_size='15sp',size_hint=(1, 0.03))
        input_area.add_widget(self.warning_message)

        create_timeline_btn = Button(text="Create timeline",size_hint=(1, 0.05))
        create_timeline_btn.bind(on_press=self.create_timeline)
        input_area.add_widget(create_timeline_btn)

        input_area.add_widget(Label(text='',size_hint=(1, 0.03)))
        
        cancel_btn = Button(text="Cancel",size_hint=(1, 0.05))
        cancel_btn.bind(on_press=self.cancel_create)
        input_area.add_widget(cancel_btn)


        layout.add_widget(input_area)
        self.add_widget(layout)

    def create_timeline(self, instance):
        new_timeline = self.timeline_name.text
        os.chdir('timelines')
        path = os.path.join(os.getcwd(), new_timeline)
        if not os.path.exists(path):
            os.mkdir(path)
            os.chdir(path)
            f = open("TimelineList.json", "w")
            TimelineListContent = """{\n    "fileType": "timeline",\n    "timeline": [\n    ]\n}"""           
            f.write(TimelineListContent)
            f.close()   

            self.timeline_name.text = ''                    
            self.manager.current = 'edit timeline'                      
        else:
            self.warning_message.text = "A timeline with same name is already created"
 
    def cancel_create(self, instance):
        self.timeline_name.text = ''
        self.manager.current = 'home'