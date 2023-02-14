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
from kivy.factory import Factory
from kivy.uix.image import Image

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
        self.modify_timeline()
        self.create_exercise_json()

    def modify_timeline(self):
        with open("TimelineList.json",'r+') as file:
          # First we load existing data into a dict.
            timeline_data = json.load(file)
            
            # python object to be appended
            new_exercise = {"exercise": self.exercise_name.text+".json"}
            
            # appending the data
            timeline_data["timeline"].append(new_exercise)
            
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(timeline_data, file, indent = 4)

    def create_exercise_json(self):
        with open(self.exercise_name.text+".json",'w') as file:
            # First we load existing data into a dict.
            content = { "fileType":"body",
                        "videoLink":self.exercise_video_link.text,
                        "keyframes":[]}
            
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(content, file, indent = 4)

    def cancel(self, instance):
        with open("TimelineList.json", 'r') as f:
            pathJson = json.load(f)
        timeline = pathJson.get("timeline")

        Item = Factory.MyDraggableItem
        Item()
        editTimeline = self.manager.get_screen('edit timeline')
        add_widget = editTimeline.exerciseLayout.ids.ReorderableLayout.add_widget
        
        for exercise in timeline:              
            add_widget(Item(text=exercise.get("exercise").replace('.json', ''), size_hint=(0.2,0.4), pos_hint={'center_y': 0.5, 'center_x': 0.5}))
            current_dir = os.getcwd()
            os.chdir("../..")
            arrow = Image(source = 'graphics/whiteArrow.png', size_hint=(None,None), pos_hint={'center_y': 0.5, 'center_x': 0.5}) 
            add_widget(arrow)
            os.chdir(current_dir)

        self.manager.current = 'edit timeline'