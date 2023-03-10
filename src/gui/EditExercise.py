import mediapipe as mp
from kivy.clock import Clock
import cv2
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
import json

import os
from kivy.factory import Factory

import src.helper

from kivy.graphics import Ellipse, Color, Line, Rectangle, Triangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup

import src.gui.EditTimeline

key_frame_index_result = []

exercise_json_content = {}

frame_list = []

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class EditExercise(Screen):
    def __init__(self, **kwargs):

        super(EditExercise, self).__init__(**kwargs) 

        self.exercise_name = ""
        self.exercise_video_link = ""
        self.frame_index = 1
        self.point_counter = 1
        self.frame_points = []

        self.preloaded_json_content = ""
        self.current_keyframe_index = 0
        self.current_point_index = 0

        width = Window.width
        height = Window.height

        self.root = BoxLayout(orientation = 'vertical')

        #self.root = FloatLayout(size=Window.size)
        self.add_widget(self.root)
        # Bind the size of the BoxLayout to the size of the Window
        Window.bind(on_resize=self.setter)

        # the top side of the screen, including exercise name and frame index
        top_area = BoxLayout(orientation='horizontal', size_hint=(1, 0.07))
        self.root.add_widget(top_area)
        # show the exercise name
        self.name_label = Label(text=self.exercise_name, 
                                  font_size='25sp')
        top_area.add_widget(self.name_label)
        # show the frame index
        self.frame_index_label = Label(text='Current frame:' + str(self.frame_index) + " Current point:" + str(self.point_counter), 
                                  font_size='25sp')
        top_area.add_widget(self.frame_index_label)
        # draw a line to show the boundry
        """with top_area.canvas:
            Line(points=[0, height*9/10, 
                         width, height*9/10], 
                         width=1)"""
        
        # the bottom side of the screen, including left area and right area
        bottom_area = BoxLayout(orientation='horizontal')
        self.root.add_widget(bottom_area)
        # draw a line to show the boundry
        """with bottom_area.canvas:
            Line(points=[width/2, 0, 
                         width/2, height*9/10], 
                         width=1)"""

        # the left side of the bottom area, including label, image and button of recording frame
        left_side = GridLayout(cols=1, size_hint=(1, 1))
        bottom_area.add_widget(left_side)
        #label_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        left_side.add_widget(Label(text='Recorded frame',
                                   font_size='25sp',
                                   size_hint=(.8, .2)))
        #left_side.add_widget(label_anchor)
        # this image is used to show gestures catched by camera
        self.img1 = Image(size_hint=(1, 3.2), 
                          allow_stretch=True, 
                          keep_ratio=True)
        #image_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        #image_anchor.add_widget(self.img1)
        left_side.add_widget(self.img1)
        record_frame_btn = Button(text="Record frame",
                                  size_hint=(1, .25))
        record_frame_btn.bind(on_press=self.record_frame)
        #rf_btn_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom')
        left_side.add_widget(record_frame_btn)
        #left_side.add_widget(rf_btn_anchor)

        # the right side of the bottom area, including label, image and button of recording frame
        right_side = GridLayout(cols=1, size_hint=(1, 1))
        bottom_area.add_widget(right_side)

        typeList = ['triPointAngle' , 'pointPosition', 'parallelLines', 'abovePosition']
        self.dropdownbutton = Button(text='Choose a point type', font_size='15sp', size_hint=(1, 0.3))
        right_side.add_widget(self.dropdownbutton)
        self.dropdown = DropDown()
        self.dropdownbutton.bind(on_release=self.dropdown.open)
        for x in range(len(typeList)):
                btn = Button(text=typeList[x].strip(), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                btn.bind(on_release=self.update_right_side)
                self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.dropdownbutton, 'text', x))

        right_side.add_widget(Label(text='Select target index', 
                                    font_size='15sp',
                                    size_hint=(1, 0.2)))
     
        body_box = BoxLayout(size_hint=(2, 2))
        right_side.add_widget(body_box)
        current_dir = os.getcwd()
        print(current_dir)
        os.chdir("..")
        body_box.add_widget(Image(source='graphics/body_index.png',
                                     allow_stretch=True, 
                                     keep_ratio=True,
                                     size_hint=(1,1)))
        os.chdir(current_dir)

        self.index_input_box = GridLayout(cols=2, size_hint_y=None)
        self.index_input_box.bind(minimum_height=self.index_input_box.setter("height"))

        self.scrollview = ScrollView(size_hint=(1, 1),pos_hint={'center_y': 0.5, 'center_x': 0.5})
        self.scrollview.add_widget(self.index_input_box)
        right_side.add_widget(self.scrollview)

        leniency = GridLayout(cols=1, size_hint=(0.5, 0.9))
        right_side.add_widget(leniency)
        leniency.add_widget(Label(text='Leniency', font_size='15sp', size_hint=(0.5, 0.3)))
        self.leniency_value = Label(text='0.0', font_size='15sp', size_hint=(0.5, 0.3))
        leniency.add_widget(self.leniency_value)
        self.slider = Slider(min=0, max=1, value=0, size_hint=(0.5, 0.7))
        self.slider.bind(on_touch_move=self.move_slider)
        leniency.add_widget(self.slider)

        next_point_btn = Button(text="Next point",
                        size_hint=(.5, .3))
        next_point_btn.bind(on_press=self.next_point)
        right_side.add_widget(next_point_btn)

        btn_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        right_side.add_widget(btn_box)
        reset_btn = Button(text="Reset exercise",
                           size_hint=(1, 0.7))
        reset_btn.bind(on_press=self.reset)
        btn_box.add_widget(reset_btn)
        self.next_btn = Button(text="Next frame",
                          size_hint=(1, 0.7))
        self.next_btn.bind(on_press=self.next)
        btn_box.add_widget(self.next_btn)
        complete_btn = Button(text="Complete exercise",
                              size_hint=(1, 0.7))
        complete_btn.bind(on_press=self.complete)
        btn_box.add_widget(complete_btn)
    
    def update_right_side(self, instance):
        self.index_input_box.clear_widgets()
        if instance.text == 'triPointAngle':
            self.index_input_box.add_widget(Label(text='Start', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.start_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.start_index)
            self.index_input_box.add_widget(Label(text='Middle', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.middle_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.middle_index)
            self.index_input_box.add_widget(Label(text='End', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.end_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.end_index)
        elif instance.text == 'pointPosition':
            self.index_input_box.add_widget(Label(text='Point', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.point_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.point_index)
        elif instance.text == 'parallelLines':
            self.index_input_box.add_widget(Label(text='Arm1 point 1', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.a1_point1_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.a1_point1_index)
            self.index_input_box.add_widget(Label(text='Arm1 point 2', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.a1_point2_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.a1_point2_index)
            
            self.index_input_box.add_widget(Label(text='Arm2 point 1', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.a2_point1_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.a2_point1_index)
            self.index_input_box.add_widget(Label(text='Arm2 point 2', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.a2_point2_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.a2_point2_index)
        elif instance.text == 'abovePosition':
            self.index_input_box.add_widget(Label(text='Above point', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.above_point_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.above_point_index)
            self.index_input_box.add_widget(Label(text='Below point', size_hint=(0.5, None), height=40, font_size='25sp'))
            self.below_point_index = TextInput(text='', size_hint=(0.5, None), write_tab=False, multiline=False, height=40, font_size='25sp')
            self.index_input_box.add_widget(self.below_point_index)

    def edit_relationship(self, instance):
        self.dropdownbutton.text = instance.text

    def setter(self, window, width, height):
        self.scrollview.width = 0#width
        self.scrollview.height = 0#height

    def record_frame(self, instance):
        self.manager.get_screen('record frame').start_update()
        self.manager.current = 'record frame'
        
    def move_slider(self, *args):
        self.leniency_value.text = str(round(self.slider.value, 2))

    def next_point(self, instance):
        if(self.preloaded_json_content!=""):
            self.current_point_index+=1
        point = {}
        final_index = []
        #valid_input = True
        for widget in self.index_input_box.children:
            if(str(type(widget))=="<class 'kivy.uix.textinput.TextInput'>"):
                valid_input = self.check_index_input(widget.text)
                if valid_input == False:
                    break
                final_index.append(int(widget.text))

        target_index = {"toTrack": final_index}     
        
        #try:
        if src.helper.CheckWithinFrame(target_index,key_frame_index_result.landmark):
            #Targeted index in frame
            #Pointtpe is triPointAngle
            if self.dropdownbutton.text == 'triPointAngle':
                target = src.helper.GoalAngle(target_index,key_frame_index_result.landmark)
                point["pointType"] = self.dropdownbutton.text
                point["toTrack"] = final_index
                point["angle"] = target
                point["leniency"] = target*round(self.slider.value, 2)
                self.frame_points.append(point)
            #Pointtpe is triPointAngle
            elif self.dropdownbutton.text == 'pointPosition':
                target = src.helper.GoalTarget(target_index,key_frame_index_result.landmark)
                point["pointType"] = self.dropdownbutton.text
                point["toTrack"] = final_index
                point["target"] = target
                point["leniency"] = round(self.slider.value, 2)
                self.frame_points.append(point)
            #Pointtpe is parallelPosition
            elif self.dropdownbutton.text == 'parallelPosition':
                point["pointType"] = self.dropdownbutton.text
                point["toTrack"] = final_index
                point["leniency"] = round(self.slider.value, 2)
                self.frame_points.append(point)
            #Pointtpe is abovePosition
            elif self.dropdownbutton.text == 'abovePosition':
                point["pointType"] = self.dropdownbutton.text
                point["toTrack"] = final_index
                point["leniency"] = round(self.slider.value, 2)
                self.frame_points.append(point)
            #Reset right side
            self.index_input_box.clear_widgets()
            self.dropdownbutton.text='Choose a point type'
            self.slider.value = 0
            self.leniency_value.text = '0.0'
            self.update_keyframe_data()
        #Targeted index out of frame
        else:
            self.call_pops()
            self.pop_content.text = 'Targeted index out of frame'
        # No recording 
        """except:
            self.call_pops()
            self.pop_content.text = 'No exercise recorded'"""
            

    def reset(self, instance):
        frame_list.clear()
    
    def next(self, instance):
        if self.frame_points:
            self.frame_index+=1
            self.point_counter=0
            self.frame_index_label.text='Current frame:' + str(self.frame_index) + " Current point:" + str(self.point_counter)
            src.gui.EditExercise.key_frame_index_result = []
            #frame_list.clear()
            self.img1.texture = None
            self.time_limit_pops()
        else: 
            self.call_pops()
            self.pop_content.text = "No point selected"

    def complete(self, instance):
        exercise_json_content["keyframes"] = frame_list
        #src.gui.EditTimeline.exercise_name_list.append(self.name_label.text)
        
        #Create exercise json
        with open(self.exercise_name+".json",'w') as file:
            file.seek(0)
            json.dump(exercise_json_content, file, indent = 4)
            file.close()
        #src.gui.EditTimeline.exercise_json.append(exercise_json_content)
        #print(src.gui.EditTimeline.exercise_json)
        with open("TimelineList.json", 'r') as file:
            timeline_data = json.load(file)
            new_exercise = {"exercise": self.name_label.text+".json"}
            timeline_data["timeline"].append(new_exercise)
            file.close()
        with open("TimelineList.json", 'w') as file:
            file.seek(0)
            json.dump(timeline_data, file, indent = 4)
            file.close()

        timeline = timeline_data.get("timeline")

        Item = Factory.MyDraggableItem
        Item()
        editTimeline = self.manager.get_screen('edit timeline')
        add_widget = editTimeline.exerciseLayout.ids.ReorderableLayout.add_widget
        
        for exercise in timeline:              
            item=Item(text=exercise.get("exercise").replace('.json',''), size_hint=(0.2,0.4), pos_hint={'center_y': 0.5, 'center_x': 0.5})
            item.ids.editButton.bind(on_press=self.edit)
            item.ids.testButton.bind(on_press=self.test)
            item.ids.deleteButton.bind(on_press=self.delete)
            add_widget(item)

        src.gui.EditExercise.key_frame_index_result = []
        #exercise_json_content=None
        frame_list.clear()
        self.img1.texture = None
        self.frame_index = 1
        self.frame_index_label.text='Current frame:' + str(self.frame_index)

        self.manager.current = 'edit timeline'
        self.preloaded_json_content = ""
        self.current_keyframe_index = 0
        self.current_point_index = 0

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
    
    def refresh(self):
        self.name_label.text = self.exercise_name

    def check_index_input(self, input):
        index_list = ["11","12","13","14","15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]
        if input not in index_list or input == None:        
            self.call_pops()
            self.pop_content.text = "Invalid index: " + input
            return False
        return True

    def update_exercise_json(self, time_limit): 
        #exercise_json_content["keyframes"].append({"points": self.frame_points,"timeLimit" : time_limit})
        frame_list.append({"points": self.frame_points,"timeLimit" : time_limit})
        
        #print(exercise_json_content)

    def call_pops(self):
        # create content and add to the popup
        self.pop_content = Button(text='')
        popup = Popup(title = "Warning!", content=self.pop_content, size_hint=(0.5,0.2), auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        self.pop_content.bind(on_press=popup.dismiss)

        # open the popup
        popup.open()

    def time_limit_pops(self):
        time_limit_box = BoxLayout(orientation='vertical')

        if(self.preloaded_json_content!=""):
            self.current_keyframe_index+=1
            self.time_limit_input = TextInput(text=self.timeLimit, multiline=False)   
        else:
            self.time_limit_input = TextInput(text="", multiline=False)   

        time_limit_box.add_widget(self.time_limit_input) 
        
        self.cfm_btn = Button(text='Confirm')
        time_limit_box.add_widget(self.cfm_btn)               

        self.time_popup = Popup(title = "Enter a time limit value (sec), leave empty if no limit", content=time_limit_box, size_hint=(0.5,0.2), auto_dismiss=False)
        
        self.cfm_btn.bind(on_press=self.time_popup.dismiss)
        self.cfm_btn.bind(on_press=self.update_time_limit)
        # open the popup
        self.time_popup.open()

    def update_time_limit(self, instance):
        if self.time_limit_input.text:
            try:
                time_limit = int(self.time_limit_input.text)
                self.update_exercise_json(time_limit)
                self.frame_points = []
            except:
                self.time_limit_pops()
                self.time_popup.title = "Invalid timelimit"
        else:
            time_limit = -1
            self.update_exercise_json(time_limit)
            self.frame_points = []

        if(self.preloaded_json_content!=""):
            self.current_point_index = 0
            self.update_keyframe_data()
            
    
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
    
    def update_keyframe_data(self):
        if(self.preloaded_json_content!=""):
            pathJson = json.loads(self.preloaded_json_content)
            keyframes = pathJson.get("keyframes")

            if(self.current_keyframe_index<len(keyframes)):
                keyframe = keyframes[self.current_keyframe_index]
                pointList = keyframe.get("points")
                if(self.current_point_index<len(pointList)):
                    points = keyframe.get("points")[self.current_point_index]

                    self.index_input_box.clear_widgets()

                    pointType = points.get("pointType")
                    self.dropdownbutton.text = pointType

                    if(pointType=='triPointAngle'):
                        self.index_input_box.add_widget(Label(text='Start', size_hint=(0.2, None)))
                        self.start_index = TextInput(text=str(points.get("toTrack")[0]),size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.start_index)
                        self.index_input_box.add_widget(Label(text='Middle', size_hint=(0.2, None)))
                        self.middle_index = TextInput(text=str(points.get("toTrack")[1]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.middle_index)
                        self.index_input_box.add_widget(Label(text='End', size_hint=(0.2, None)))
                        self.end_index = TextInput(text=str(points.get("toTrack")[2]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.end_index)
                    
                    elif(pointType=='pointPosition'):
                        self.index_input_box.add_widget(Label(text='Point', size_hint=(0.2, None)))
                        self.point_index = TextInput(text=str(points.get("toTrack")[0]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.point_index)
                    
                    elif(pointType=='parallelPosition'):
                        self.index_input_box.add_widget(Label(text='Arm1 point 1', size_hint=(0.2, None)))
                        self.a1_point1_index = TextInput(text=str(points.get("toTrack")[0]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.a1_point1_index)
                        self.index_input_box.add_widget(Label(text='Arm1 point 2', size_hint=(0.2, None)))
                        self.a1_point2_index = TextInput(text=str(points.get("toTrack")[1]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.a1_point2_index)

                        self.index_input_box.add_widget(Label(text='Arm2 point 1', size_hint=(0.2, None)))
                        self.a2_point1_index = TextInput(text=str(points.get("toTrack")[2]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.a2_point1_index)
                        self.index_input_box.add_widget(Label(text='Arm2 point 2', size_hint=(0.2, None)))
                        self.a2_point2_index = TextInput(text=str(points.get("toTrack")[3]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.a2_point2_index)

                    elif(pointType=='abovePosition'):
                        self.index_input_box.add_widget(Label(text='Above point', size_hint=(0.2, None)))
                        self.above_point_index = TextInput(text=str(points.get("toTrack")[0]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.above_point_index)
                        self.index_input_box.add_widget(Label(text='Below point', size_hint=(0.2, None)))
                        self.below_point_index = TextInput(text=str(points.get("toTrack")[1]), size_hint=(0.8, None), multiline=False)
                        self.index_input_box.add_widget(self.below_point_index)
                    
                    self.slider.value = points.get("leniency")
                    self.move_slider()
                    self.timeLimit=str(keyframe.get("timeLimit"))