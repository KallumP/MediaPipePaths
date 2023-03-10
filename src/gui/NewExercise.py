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
from kivy.uix.popup import Popup

import src.gui.EditExercise
import src.gui.SelectTimeline

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

        self.exercise_name = TextInput(text = '', font_size = '25sp', size_hint = (1, 0.3), write_tab=False, multiline = False)
        input_area.add_widget(self.exercise_name)

        input_area.add_widget(Label(text='Exercise video link', font_size='20sp',size_hint=(1, 0.2)))

        self.exercise_video_link = TextInput(text = '', font_size = '25sp', size_hint = (1, 0.3), write_tab=False, multiline = False)
        input_area.add_widget(self.exercise_video_link)

        input_area.add_widget(Label(text='Repeat', font_size='20sp' ,size_hint=(1, 0.2)))

        self.repeat_times = TextInput(text = '1', font_size = '25sp', size_hint = (1, 0.3), write_tab=False, multiline = False)
        input_area.add_widget(self.repeat_times)

        self.layout.add_widget(input_area)
        
        add_exercise_btn = Button(text="New exercise",size_hint=(0.5, 0.08),pos_hint={'center_y': 0.2, 'center_x': 0.5})
        add_exercise_btn.bind(on_press=self.create_exercise)
        self.layout.add_widget(add_exercise_btn)

        cancel_btn = Button(text="Cancel",size_hint=(0.5, 0.08),pos_hint={'center_y': 0.1, 'center_x': 0.5})
        cancel_btn.bind(on_press=self.cancel)
        self.layout.add_widget(cancel_btn)

        self.add_widget(self.layout)

    def create_exercise(self, instance):
        #not self.repeat_times.text.replace(".", "").isnumeric()
        if self.repeat_times.text.isnumeric() and self.exercise_name.text != "" and self.exercise_video_link.text != "":
            #self.modify_timeline()
            self.create_exercise_json()
            self.manager.get_screen('edit exercise').exercise_name = str(self.exercise_name.text)
            self.manager.get_screen('edit exercise').exercise_video_link = str(self.exercise_video_link.text)

            self.exercise_name.text = ""
            self.exercise_video_link.text = ""
            self.repeat_times.text = "1"
            
            self.manager.current = 'edit exercise'
            self.manager.get_screen('edit exercise').refresh()
        else: 
            self.call_pops()
        

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
        #with open(self.exercise_name.text+".json",'w') as file:
            # First we load existing data into a dict.            
            
        repeat_value = self.repeat_times.text                   

        content = { "fileType":"body",
                    "videoLink":self.exercise_video_link.text,
                    "repeat": repeat_value,
                    "keyframes":[]}
        
        src.gui.EditExercise.exercise_json_content = content
            
            # Sets file's current position at offset.
            #file.seek(0)
            # convert back to json.
            #json.dump(content, file, indent = 4)
        

    def cancel(self, instance):
        with open("TimelineList.json", 'r') as f:
            pathJson = json.load(f)
        timeline = pathJson.get("timeline")

        Item = Factory.MyDraggableItem
        Item()
        editTimeline = self.manager.get_screen('edit timeline')
        add_widget = editTimeline.exerciseLayout.ids.ReorderableLayout.add_widget
        
        for exercise in timeline:              
            item=Item(text=exercise.get("exercise").replace('.json', ''), size_hint=(0.2,0.4), pos_hint={'center_y': 0.5, 'center_x': 0.5})
            item.ids.editButton.bind(on_press=self.edit)
            item.ids.deleteButton.bind(on_press=self.delete)
            add_widget(item)

        self.manager.current = 'edit timeline'

    def call_pops(self):
        # create content and add to the popup
        content = Button(text='Invalid exercise name or repeat value')
        popup = Popup(title = "Warning!", content=content, size_hint=(0.5,0.2), auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        content.bind(on_press=popup.dismiss)

        # open the popup
        popup.open()

    def edit(self, instance):
        editExercise = self.manager.get_screen('edit exercise')
        self.manager.current = 'edit exercise'

        #Setting the name of the JSON file to edit
        filePath = instance.parent.parent.text+'.json'
        editExercise.exercise_name = instance.parent.parent.text
        
        global pathJson
        with open(filePath, 'r') as f:
            pathJson = json.load(f)
        
        #Storing json string in editExercise
        #Initialising values
        json_string = json.dumps(pathJson)
        editExercise.preloaded_json_content = json_string
        editExercise.current_keyframe_index = 0
        editExercise.current_point_index = 0
        
        #Parsing JSON files
        keyframes = pathJson.get("keyframes")
        editExercise.exercise_video_link=pathJson.get("videoLink")
        keyframe = keyframes[editExercise.current_keyframe_index]
        points = keyframe.get("points")[editExercise.current_point_index]

        pointType = points.get("pointType")
        editExercise.dropdownbutton.text = pointType

        if(pointType=='triPointAngle'):
            editExercise.index_input_box.add_widget(Label(text='Start', size_hint=(0.2, None)))
            editExercise.start_index = TextInput(text=str(points.get("toTrack")[0]),size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.start_index)
            editExercise.index_input_box.add_widget(Label(text='Middle', size_hint=(0.2, None)))
            editExercise.middle_index = TextInput(text=str(points.get("toTrack")[1]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.middle_index)
            editExercise.index_input_box.add_widget(Label(text='End', size_hint=(0.2, None)))
            editExercise.end_index = TextInput(text=str(points.get("toTrack")[2]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.end_index)
        
        elif(pointType=='pointPosition'):
            editExercise.index_input_box.add_widget(Label(text='Point', size_hint=(0.2, None)))
            editExercise.point_index = TextInput(text=str(points.get("toTrack")[0]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.point_index)
        
        elif(pointType=='parallelPosition'):
            editExercise.index_input_box.add_widget(Label(text='Arm1 point 1', size_hint=(0.2, None)))
            editExercise.a1_point1_index = TextInput(text=str(points.get("toTrack")[0]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.a1_point1_index)
            editExercise.index_input_box.add_widget(Label(text='Arm1 point 2', size_hint=(0.2, None)))
            editExercise.a1_point2_index = TextInput(text=str(points.get("toTrack")[1]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.a1_point2_index)

            editExercise.index_input_box.add_widget(Label(text='Arm2 point 1', size_hint=(0.2, None)))
            editExercise.a2_point1_index = TextInput(text=str(points.get("toTrack")[2]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.a2_point1_index)
            editExercise.index_input_box.add_widget(Label(text='Arm2 point 2', size_hint=(0.2, None)))
            editExercise.a2_point2_index = TextInput(text=str(points.get("toTrack")[3]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.a2_point2_index)

        elif(pointType=='abovePosition'):
            editExercise.index_input_box.add_widget(Label(text='Above point', size_hint=(0.2, None)))
            editExercise.above_point_index = TextInput(text=str(points.get("toTrack")[0]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.above_point_index)
            editExercise.index_input_box.add_widget(Label(text='Below point', size_hint=(0.2, None)))
            editExercise.below_point_index = TextInput(text=str(points.get("toTrack")[1]), size_hint=(0.8, None), multiline=False)
            editExercise.index_input_box.add_widget(editExercise.below_point_index)
        
        editExercise.slider.value = points.get("leniency")
        editExercise.move_slider()
        editExercise.timeLimit=str(keyframe.get("timeLimit"))
    
    def delete(self, instance):
        #Instance refers to the Button, while its parent is the BoxLayout within which the Button is contained
        #We need to remove the DraggableItem itself, which is the parent of the BoxLayout
        #We remove this DraggableItem from its parent, that is the ReorderableLayout
        itemToBeRemoved = instance.parent.parent
        layoutToRemoveFrom = itemToBeRemoved.parent
        layoutToRemoveFrom.remove_widget(itemToBeRemoved)