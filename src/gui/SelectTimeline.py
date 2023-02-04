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

class SelectTimeline(Screen):
    def __init__(self, **kwargs):
        super(SelectTimeline, self).__init__(**kwargs) 
        self.layout = FloatLayout()
        self.scrollview = None
        
        self.layout.add_widget(Button(text='refresh',size_hint=(0.5, 0.05),pos_hint={'center_y': 0.2, 'center_x': 0.5},on_press=self.refresh))
        
        cancel_btn = Button(text="Cancel",size_hint=(1, 0.05))
        cancel_btn.bind(on_press=self.cancel_create)
        self.layout.add_widget(cancel_btn)

        self.add_widget(self.layout)
        
        self.list_scenarios()

    def list_scenarios(self):
        if self.scrollview: self.remove_widget(self.scrollview) 
        
        os.chdir('timelines')
        timelines = [f for f in listdir('.') if isfile(join('.', f))]
        os.chdir('..')

        button_area = GridLayout(cols=1, size_hint_y=None)
        button_area.bind(minimum_height=button_area.setter("height"))
        for timeline in timelines:
            timeline = timeline.replace('.json', '')
            timeline_btn = Button(text=timeline, size_hint=(0.5, None))
            timeline_btn.bind(on_press=self.open_timeline)
            button_area.add_widget(timeline_btn)

        self.scrollview = ScrollView(size_hint=(0.5, 0.5),pos_hint={'center_y': 0.5, 'center_x': 0.5})
        self.scrollview.add_widget(button_area)
        self.layout.add_widget(self.scrollview)

    def refresh(self, instance):
        if self.scrollview: self.layout.remove_widget(self.scrollview) 
        self.list_scenarios()

    def open_timeline(self, instance):
        os.chdir('timelines')
        filePath = str(instance.text) + ".json"

        #global pathJson
        with open(filePath, 'r') as f:
            pathJson = json.load(f)

        fileType = pathJson.get("fileType")
        os.chdir('..')
        return fileType == "body", pathJson

    def cancel_create(self, instance):
        self.manager.current = 'home'