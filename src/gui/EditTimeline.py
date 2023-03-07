from imp import reload
from re import L, template
import re
from turtle import onclick
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
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
import win32api 
from kivy.uix.label import Label
from kivy.uix.image import Image

import firebase_admin
from firebase_admin import db
import main
firebase_admin.initialize_app(main.cred, {
            'databaseURL':"https://motion-9821b-default-rtdb.europe-west1.firebasedatabase.app/"
            })

KV_CODE = '''
<MyReorderableLayout@KXReorderableBehavior+BoxLayout>:
    spacing: 10
    padding: 10
    cols: 4
    drag_classes: ['test', ]
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
ScrollView:
    MyReorderableLayout:
        id: ReorderableLayout
        size_hint_min: self.minimum_size
'''

timeline_name = ""
exercise_name_list = []
exercise_json = []


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class EditTimeline(Screen):
    def __init__(self, **kwargs):
        super(EditTimeline, self).__init__(**kwargs) 
        
        self.layout = BoxLayout(orientation='vertical')  

        self.bannerLayout = GridLayout(cols=2, size_hint=(1, 0.4))
        self.title_text = Label(text='Edit timeline - ', font_size = '50sp', markup=True)
        self.bannerLayout.add_widget(self.title_text)

        self.buttonLayout = BoxLayout(orientation='vertical', size_hint_x = None, width = 100)

        self.saveButton = Button(text="Save Timeline")
        self.saveButton.bind(on_press=self.saveTimeline)
        self.buttonLayout.add_widget(self.saveButton)

        self.addExercise_btn = Button(text="Add exercise")
        self.addExercise_btn.bind(on_press=self.add_exercise)
        self.buttonLayout.add_widget(self.addExercise_btn)

        self.bannerLayout.add_widget(self.buttonLayout)

        self.layout.add_widget(self.bannerLayout)

        #self.layout.add_widget(self.title_text)

        current_dir = os.getcwd()
        os.chdir("..")
        arrow = Image(source = 'graphics/longWhiteArrow.png', size_hint_x=0.5, pos_hint={'center_y': 0.5, 'center_x': 0.5}) 
        self.layout.add_widget(arrow)
        os.chdir(current_dir)

        self.content_layout = BoxLayout(orientation='horizontal', spacing=10)

        self.exerciseLayout = Builder.load_string(KV_CODE)
        self.on_start()

        self.content_layout.add_widget(self.exerciseLayout)
        #self.layout.add_widget(self.exerciseLayout)
        #self.layout.add_widget(self.buttonLayout)

        self.layout.add_widget(self.content_layout)

        padding = Label(text="")
        self.layout.add_widget(padding)

        self.add_widget(self.layout)

    def on_start(self):
        Item = Factory.MyDraggableItem
        Item()
        add_widget = self.exerciseLayout.ids.ReorderableLayout.add_widget
    
    def saveTimeline(self, instance):
        updatedList=[]
        for widget in self.exerciseLayout.ids.ReorderableLayout.children:
            if(str(type(widget))=="<class 'kivy.factory.MyDraggableItem'>"):
                updatedList.insert(0, widget.text)

        self.manager.current = 'home'

        self.exerciseLayout.ids.ReorderableLayout.clear_widgets()

        
        with open("TimelineList.json",'w') as file:
            content = { "fileType":"timeline",
                        "timeline":[]}

            for exercise in updatedList:
                content["timeline"].append({"exercise":exercise + ".json"})

            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(content, file, indent = 4) 
        
        ref = db.reference("/Timelines/"+timeline_name)
        ref.set(content)
        for exercise in updatedList:
            exercise_name_list.append(exercise)
            with open(exercise + ".json", 'r') as f:
                pathJson = json.load(f)
                exercise_json.append(pathJson)
        for i in range(len(exercise_name_list)):
            ref = db.reference("/Exercises/"+exercise_name_list[i])
            ref.set(exercise_json[i])

        self.title_text.text = 'Edit timeline - '

        os.chdir('..')

    def add_exercise(self, instance):
        self.exerciseLayout.ids.ReorderableLayout.clear_widgets()
        self.manager.current = 'new exercise'
