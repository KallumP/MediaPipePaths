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

from kivy.lang import Builder
from kivy.factory import Factory
import kivy_garden.draggable

KV_CODE = '''
<MyDraggableItem@KXDraggableBehavior+Label>:
    font_size: 30
    text: root.text
    drag_timeout: 0
    drag_cls: 'test'
    canvas.after:
        Color:
            rgba: .5, 1, 0, 1 if root.is_being_dragged else .5
        Line:
            width: 2 if root.is_being_dragged else 1
            rectangle: [*self.pos, *self.size, ]
'''

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class SelectTimeline(Screen):
    def __init__(self, **kwargs):
        super(SelectTimeline, self).__init__(**kwargs) 
        Builder.load_string(KV_CODE)
        self.layout = FloatLayout()
        self.scrollview = None
        
        self.layout.add_widget(Button(text='refresh',size_hint=(0.5, 0.05),pos_hint={'center_y': 0.2, 'center_x': 0.5},on_press=self.refresh))
        
        cancel_btn = Button(text="Cancel",size_hint=(1, 0.05))
        cancel_btn.bind(on_press=self.cancel_create)
        self.layout.add_widget(cancel_btn)

        self.add_widget(self.layout)
        
        self.list_timeline()

    def list_timeline(self):
        if self.scrollview: self.remove_widget(self.scrollview) 
        
        timelines = [f for f in listdir('.')]

        button_area = GridLayout(cols=1, size_hint_y=None)
        button_area.bind(minimum_height=button_area.setter("height"))
        for timeline in timelines:
            #timeline = timeline.replace('.json', '')
            timeline_btn = Button(text=timeline, size_hint=(0.5, None))
            timeline_btn.bind(on_press=self.open_timeline)
            button_area.add_widget(timeline_btn)

        self.scrollview = ScrollView(size_hint=(0.5, 0.5),pos_hint={'center_y': 0.5, 'center_x': 0.5})
        self.scrollview.add_widget(button_area)
        self.layout.add_widget(self.scrollview)

    def refresh(self, instance):
        if self.scrollview: self.layout.remove_widget(self.scrollview) 
        self.list_timeline()

    def open_timeline(self, instance):
        os.chdir(instance.text)
        self.read_timeline(instance.text)
        self.manager.current = 'edit timeline'  
        

    def cancel_create(self, instance):
        self.manager.current = 'home'

    def read_timeline(self, timelineName):
        #try:
        with open("TimelineList.json", 'r') as f:
            pathJson = json.load(f)

        self.fileType = pathJson.get("fileType")
        self.timeline = pathJson.get("timeline")
        self.update_screen_with_timeline(timelineName)
        #except:
            #f = open("TimelineList.json", "w")
            #TimelineListContent = """{\n    "fileType": "timeline",\n    "timeline": [\n    ]\n}"""           
            #f.write(TimelineListContent)
            #f.close()  
            #self.read_timeline()

    
    def update_screen_with_timeline(self, timelineName):
        Item = Factory.MyDraggableItem
        Item()
        editTimeline = self.manager.get_screen('edit timeline')
        add_widget = editTimeline.exerciseLayout.ids.ReorderableLayout.add_widget

        editTimeline.title_text.text += timelineName
        for exercise in self.timeline:          
            add_widget(Item(text=exercise.get("exercise").replace('.json', ''), size=(100, 100), size_hint=(None,None)))