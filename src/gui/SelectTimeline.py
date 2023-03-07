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

from kivy.uix.image import Image

import os
import os.path
from os import listdir
from os.path import isfile, join
import json
import time
from kivy.lang import Builder
from kivy.factory import Factory
import kivy_garden.draggable

import src.gui.EditTimeline
import src.gui.TestExercise

KV_CODE = '''
<MyDraggableItem@KXDraggableBehavior+BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    drag_timeout: 0
    drag_cls: 'test'
    text: ''
    canvas.after:
        Color:
            rgba: .5,1,0,1 if root.is_being_dragged else .5
        Line:
            width: 2 if root.is_being_dragged else 1
            rectangle: [*self.pos, *self.size, ]
    Label:
        text: root.text
        font_size: 30
    BoxLayout:
        orientation: 'horizontal'
        Button:
            text: 'Edit'
            id: editButton
        Button:
            text: 'Test'
            id: testButton
        Button:
            text: 'Delete'
            id: deleteButton
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
        src.gui.EditTimeline.timeline_name = timelineName
        """for exercise in self.timeline:
            src.gui.EditTimeline.exercise_name_list.append(list(exercise.values())[0].replace(".json",""))
            with open(list(exercise.values())[0], 'r') as f:
                pathJson = json.load(f)
                src.gui.EditTimeline.exercise_json.append(pathJson)"""
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
            item=Item(text=exercise.get("exercise").replace('.json',''), size_hint=(0.2,0.4), pos_hint={'center_y': 0.5, 'center_x': 0.5})
            item.ids.editButton.bind(on_press=self.edit)
            item.ids.testButton.bind(on_press=self.test)
            item.ids.deleteButton.bind(on_press=self.delete)
            add_widget(item)
    
    def edit(self, instance):
        editExercise = self.manager.get_screen('edit exercise')
        
        print("Edit was pressed!")
    
    def test(self, instance):
        src.gui.TestExercise.testing = True
        src.gui.TestExercise.testing_exercise_json = instance.parent.parent.text + ".json"
        self.manager.get_screen('test exercise').start_update()
        self.manager.current = 'test exercise'
        

    def delete(self, instance):
        #Instance refers to the Button, while its parent is the BoxLayout within which the Button is contained
        #We need to remove the DraggableItem itself, which is the parent of the BoxLayout
        #We remove this DraggableItem from its parent, that is the ReorderableLayout
        itemToBeRemoved = instance.parent.parent
        layoutToRemoveFrom = itemToBeRemoved.parent
        layoutToRemoveFrom.remove_widget(itemToBeRemoved)