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
from kivy.lang import Builder
from kivy.factory import Factory
import kivy_garden.draggable

KV_CODE = '''
<MyReorderableLayout@KXReorderableBehavior+StackLayout>:
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

#Constant Variables
WIDTH = 100
HEIGHT = 50

#List for Testing - To remove and replace with Json list
#pyList = ['2', '3', '4', '5', '6']

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class EditTimeline(Screen):
    def __init__(self, **kwargs):
        super(EditTimeline, self).__init__(**kwargs) 
        self.l = Builder.load_string(KV_CODE)
        self.on_start()

        self.add_widget(self.l)

    def on_start(self):
        Item = Factory.MyDraggableItem
        Item()
        add_widget = self.l.ids.ReorderableLayout.add_widget

        #Replace with Json list
        #for i in pyList:
            #add_widget(Item(text=str(i), size=(WIDTH, HEIGHT), size_hint=(None,None)))

        saveButton = Button(text="Save Timeline", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5})
        saveButton.bind(on_press=self.saveTimeline)
        add_widget(saveButton)
    
    def saveTimeline(self, instance):
        updatedList=[]
        for widget in self.l.ids.ReorderableLayout.children:
            if(str(type(widget))=="<class 'kivy.factory.MyDraggableItem'>"):
                updatedList.insert(0, widget.text)

        f = open("TimelineList.json", "w")
        content = """{\n    "fileType": "timeline",\n    "timeline": [\n"""  

        for exercise in updatedList:
            content += """        {\n            "exercise": \"""" + exercise + """.json"\n        },\n"""

        content = content.rsplit(',', 1)[0]

        content += """\n    ]\n}"""  
        f.write(content) 
        f.close()  

        