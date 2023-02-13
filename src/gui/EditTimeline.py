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

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class EditTimeline(Screen):
    def __init__(self, **kwargs):
        super(EditTimeline, self).__init__(**kwargs) 
        Window.bind(mouse_pos=self.on_mouseover)
        self.layout = BoxLayout(orientation='vertical')

        self.bannerLayout = GridLayout(cols=2, size_hint=(1, 0.2))
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

        self.content_layout = BoxLayout(orientation='horizontal', spacing=10)

        self.exerciseLayout = Builder.load_string(KV_CODE)
        self.on_start()

        self.content_layout.add_widget(self.exerciseLayout)
        #self.layout.add_widget(self.exerciseLayout)
        #self.layout.add_widget(self.buttonLayout)

        self.layout.add_widget(self.content_layout)

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

        f = open("TimelineList.json", "w")
        content = """{\n    "fileType": "timeline",\n    "timeline": [\n"""  

        for exercise in updatedList:
            content += """        {\n            "exercise": \"""" + exercise + """.json"\n        },\n"""

        content = content.rsplit(',', 1)[0]

        content += """\n    ]\n}"""  
        f.write(content) 
        f.close()  

        self.title_text.text = 'Edit timeline - '

        os.chdir('..')

    def on_mouseover(self, window, pos):
        state_left = win32api.GetKeyState(0x01)
        for widget in self.exerciseLayout.ids.ReorderableLayout.children:
            if(str(type(widget))=="<class 'kivy.factory.MyDraggableItem'>"):
                if widget.collide_point(*pos) and state_left >= 0:
                    print(widget.pos)
    def add_exercise(self, instance):
        self.manager.current = 'new exercise'
