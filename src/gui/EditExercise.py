import mediapipe as mp
from kivy.clock import Clock
import cv2
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
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

key_frame_index_result = []

exercise_json_content = {}

frame_points = []

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class EditExercise(Screen):
    def __init__(self, **kwargs):

        super(EditExercise, self).__init__(**kwargs) 

        self.exercise_name = ""
        self.exercise_video_link = ""
        self.frame_index = 0

        width = Window.width
        height = Window.height

        self.root = FloatLayout(size=Window.size)
        self.add_widget(self.root)
        # Bind the size of the BoxLayout to the size of the Window
        Window.bind(on_resize=self.setter)

        # the top side of the screen, including exercise name and frame index
        top_area = BoxLayout(orientation='horizontal', 
                             size_hint=(1, .1), 
                             pos_hint={'top':1})
        self.root.add_widget(top_area)
        # show the exercise name
        self.name_label = Label(text=self.exercise_name, 
                                  font_size='30sp')
        top_area.add_widget(self.name_label)
        # show the frame index
        top_area.add_widget(Label(text='Current frame:' + str(self.frame_index), 
                                  font_size='30sp'))
        # draw a line to show the boundry
        with top_area.canvas:
            Line(points=[0, height*9/10, 
                         width, height*9/10], 
                         width=1)
        
        # the bottom side of the screen, including left area and right area
        bottom_area = BoxLayout(orientation='horizontal',
                                size_hint=(1, .9))
        self.root.add_widget(bottom_area)
        # draw a line to show the boundry
        with bottom_area.canvas:
            Line(points=[width/2, 0, 
                         width/2, height*9/10], 
                         width=1)

        # the left side of the bottom area, including label, image and button of recording frame
        left_side = AnchorLayout()
        bottom_area.add_widget(left_side)
        label_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        label_anchor.add_widget(Label(text='Recorded frame',
                                   font_size='25sp',
                                   size_hint=(.8, .2)))
        left_side.add_widget(label_anchor)
        # this image is used to show gestures catched by camera
        self.img1 = Image(size_hint=(.8, .4), 
                          allow_stretch=True, 
                          keep_ratio=True)
        image_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        image_anchor.add_widget(self.img1)
        left_side.add_widget(image_anchor)
        record_frame_btn = Button(text="Record frame",
                                  size_hint=(.7, .1))
        record_frame_btn.bind(on_press=self.record_frame)
        rf_btn_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom')
        rf_btn_anchor.add_widget(record_frame_btn)
        left_side.add_widget(rf_btn_anchor)

        # the right side of the bottom area, including label, image and button of recording frame
        right_side = BoxLayout(orientation='vertical')
        bottom_area.add_widget(right_side)
        label1_box = BoxLayout()
        right_side.add_widget(label1_box)
        label1_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        label1_anchor.add_widget(Label(text='Select target index', 
                                    font_size='25sp',
                                    size_hint=(.8, .2)))
        label1_box.add_widget(label1_anchor)
        
        body_box = BoxLayout()
        right_side.add_widget(body_box)
        body_box.add_widget(Image(source='src/gui/body_index.png',
                                     allow_stretch=True, 
                                     keep_ratio=True,
                                     size_hint=(1, 1.75)))
        
        # the code following is currently abandoned due to new operation design
        # with people_frame.canvas:
        #     # draw the head
        #     Line(circle=(width*3/4, height*3/4, width/24), width=1)  # draw a border around the circle
        #     # draw the body
        #     Line(points=[width*3/4-width/15, height*3/4-width/24, width*3/4+width/15, height*3/4-width/24], width=1)
        #     Line(points=[width*3/4-width/25, height*3/4-width*5/24, width*3/4+width/25, height*3/4-width*5/24], width=1)
        #     Line(points=[width*3/4-width/15, height*3/4-width/24, width*3/4-width/25, height*3/4-width*5/24], width=1)
        #     Line(points=[width*3/4+width/15, height*3/4-width/24, width*3/4+width/25, height*3/4-width*5/24], width=1)
        #     # draw the legs
        #     Line(points=[width*3/4-width/25, height*3/4-width*5/24, width*3/4-width/15, height*3/4-width*7/24], width=1)
        #     Line(points=[width*3/4+width/25, height*3/4-width*5/24, width*3/4+width/15, height*3/4-width*7/24], width=1)
        #     Line(points=[width*3/4-width/15, height*3/4-width*7/24, width*3/4-width/25, height*3/4-width*9/24], width=1)
        #     Line(points=[width*3/4+width/15, height*3/4-width*7/24, width*3/4+width/25, height*3/4-width*9/24], width=1)
        #     # draw the feet
        #     Line(points=[width*3/4-width*2/25, height*3/4-width*10/24, width*3/4-width/25, height*3/4-width*10/24], width=1)
        #     Line(points=[width*3/4-width*2/25, height*3/4-width*10/24, width*3/4-width/25, height*3/4-width*9/24], width=1)
        #     Line(points=[width*3/4-width/25, height*3/4-width*10/24, width*3/4-width/25, height*3/4-width*9/24], width=1)
        #     Line(points=[width*3/4+width*2/25, height*3/4-width*10/24, width*3/4+width/25, height*3/4-width*10/24], width=1)
        #     Line(points=[width*3/4+width*2/25, height*3/4-width*10/24, width*3/4+width/25, height*3/4-width*9/24], width=1)
        #     Line(points=[width*3/4+width/25, height*3/4-width*10/24, width*3/4+width/25, height*3/4-width*9/24], width=1)
        #     # draw the arms
        #     Line(points=[width*3/4-width/15, height*3/4-width/24, width*3/4-width/10, height*3/4-width*3/24], width=1)
        #     Line(points=[width*3/4+width/15, height*3/4-width/24, width*3/4+width/10, height*3/4-width*3/24], width=1)
        #     Line(points=[width*3/4-width/10, height*3/4-width*3/24, width*3/4-width*3/20, height*3/4-width*2/24], width=1)
        #     Line(points=[width*3/4+width/10, height*3/4-width*3/24, width*3/4+width*3/20, height*3/4-width*2/24], width=1)
        #     # draw the hands
        #     Line(points=[width*3/4-width*3/20, height*3/4-width*2/24, width*3/4-width*7/40, height*3/4-width*2/24], width=1)
        #     Line(points=[width*3/4-width*3/20, height*3/4-width*2/24, width*3/4-width*8/50, height*3/4-width*1/20], width=1)
        #     Line(points=[width*3/4-width*7/40, height*3/4-width*2/24, width*3/4-width*8/50, height*3/4-width*1/20], width=1)
        #     Line(points=[width*3/4-width*3/20, height*3/4-width*2/24, width*3/4-width*7/50, height*3/4-width*2/30], width=1)
        #     Line(points=[width*3/4+width*3/20, height*3/4-width*2/24, width*3/4+width*7/40, height*3/4-width*2/24], width=1)
        #     Line(points=[width*3/4+width*3/20, height*3/4-width*2/24, width*3/4+width*8/50, height*3/4-width*1/20], width=1)
        #     Line(points=[width*3/4+width*7/40, height*3/4-width*2/24, width*3/4+width*8/50, height*3/4-width*1/20], width=1)
        #     Line(points=[width*3/4+width*3/20, height*3/4-width*2/24, width*3/4+width*7/50, height*3/4-width*2/30], width=1)

        input_box = BoxLayout(orientation='horizontal')
        right_side.add_widget(input_box)
        box1 = BoxLayout(orientation='vertical')
        input_box.add_widget(box1)
        box1.add_widget(Label(text='Indexes',
                              font_size='15sp'))
        self.index_input1 = TextInput(text = '', font_size = '15sp', multiline = True)
        box1.add_widget(self.index_input1)

        box2 = BoxLayout(orientation='vertical')
        input_box.add_widget(box2)
        box2.add_widget(Label(text='Time Limit',
                              font_size='15sp'))
        self.index_input2 = TextInput(text = '', font_size = '15sp', multiline = True)
        box2.add_widget(self.index_input2)

        select_box = BoxLayout(orientation='horizontal')
        right_side.add_widget(select_box)
        pointtype = BoxLayout(orientation='vertical')
        select_box.add_widget(pointtype)
        pointtype.add_widget(Label(text='Point Type',
                              font_size='15sp')) 

        typeList = ['None','triPointAngle' , 'pointPosition', 'parallelPosition', 'abovePosition']
        self.dropdownbutton = Button(text='Choose a point type')
        pointtype.add_widget(self.dropdownbutton)
        self.dropdown = DropDown()
        self.dropdownbutton.bind(on_release=self.dropdown.open)
        for x in range(len(typeList)):
                btn = Button(text=typeList[x].strip(), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.dropdownbutton, 'text', x))

        leniency = BoxLayout(orientation='vertical')
        select_box.add_widget(leniency)
        leniency.add_widget(Label(text='Leniency',
                              font_size='15sp'))
        self.leniency_value = Label(text='0.0', font_size='15sp')
        leniency.add_widget(self.leniency_value)
        self.slider = Slider(min=0, max=1, value=0)
        self.slider.bind(on_touch_move=self.move_slider)
        leniency.add_widget(self.slider)

        ok_box = BoxLayout(orientation='horizontal')
        right_side.add_widget(ok_box)
        ok_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        ok_btn = Button(text="OK",
                        size_hint=(.5, .3))
        ok_btn.bind(on_press=self.ok)
        ok_anchor.add_widget(ok_btn)
        ok_box.add_widget(ok_anchor)
        
        btn_box = BoxLayout(orientation='horizontal')
        right_side.add_widget(btn_box)
        reset_btn = Button(text="Reset exercise",
                           size_hint=(1, .2))
        reset_btn.bind(on_press=self.reset)
        btn_box.add_widget(reset_btn)
        next_btn = Button(text="Next frame",
                          size_hint=(1, .2))
        next_btn.bind(on_press=self.next)
        btn_box.add_widget(next_btn)
        complete_btn = Button(text="Complete exercise",
                              size_hint=(1, .2))
        complete_btn.bind(on_press=self.complete)
        btn_box.add_widget(complete_btn)
        
    def edit_relationship(self, instance):
        self.dropdownbutton.text = instance.text

    def setter(self, window, width, height):
        self.root.width = width
        self.root.height = height

    def record_frame(self, instance):
        self.manager.current = 'record frame'
        
    def move_slider(self, *args):
        self.leniency_value.text = str(round(self.slider.value, 2))

    def ok(self, instance):
        point = {}

        # indexes
        split_index = self.index_input1.text.split()    
        final_index = []
        for x in split_index:
            x = x.replace('\n', '')
            x = x.replace(';', '')
            final_index.append(int(x))
        #point["toTrack"] = final_index
        target_index = {"toTrack": final_index}

        try:
            if src.helper.CheckWithinFrame(target_index,key_frame_index_result.landmark):
                #Targeted index in frame
                #Pointtpe is triPointAngle
                if self.dropdownbutton.text == 'triPointAngle':
                    if len(final_index) != 3:
                        self.call_pops()
                        self.pop_content.text = 'Only 3 index should be selected'
                    else:
                        target = src.helper.WithinAngle(target_index,key_frame_index_result.landmark)
                        point["pointType"] = self.dropdownbutton.text
                        point["toTrack"] = final_index
                        point["angle"] = target
                        point["leniency"] = target*round(self.slider.value, 2)
                        frame_points.append(point)
                #Pointtpe is triPointAngle
                elif self.dropdownbutton.text == 'pointPosition':
                    if len(final_index) != 1:
                        self.call_pops()
                        self.pop_content.text = 'Only 1 index should be selected'
                    else:
                        target = src.helper.WithinTarget(target_index,key_frame_index_result.landmark)
                        point["pointType"] = self.dropdownbutton.text
                        point["toTrack"] = final_index
                        point["target"] = target
                        point["leniency"] = target*round(self.slider.value, 2)
                        frame_points.append(point)
                #Pointtpe is parallelPosition
                elif self.dropdownbutton.text == 'parallelPosition':
                    if len(final_index) != 4:
                        self.call_pops()
                        self.pop_content.text = 'Only 4 index should be selected'
                    else:
                        point["pointType"] = self.dropdownbutton.text
                        point["toTrack"] = final_index
                        point["leniency"] = round(self.slider.value, 2)
                        frame_points.append(point)
                #Pointtpe is abovePosition
                elif self.dropdownbutton.text == 'abovePosition':
                    if len(final_index) != 2:
                        self.call_pops()
                        self.pop_content.text = 'Only 2 index should be selected'
                    else:
                        point["pointType"] = self.dropdownbutton.text
                        point["toTrack"] = final_index
                        point["leniency"] = round(self.slider.value, 2)
                        frame_points.append(point)
            #Targeted index out of frame
            else:
                self.call_pops()
                self.pop_content.text = 'Targeted index out of frame'
        # No recording 
        except:
            self.call_pops()
            self.pop_content.text = 'No exercise recorded'
    
    def reset(self, instance):
        return 1
    
    def next(self, instance):
        self.update_exercise_json()
        #return 1
        

    def complete(self, instance):
        #Create exercise json
        with open(self.exercise_name+".json",'w') as file:
            file.seek(0)
            json.dump(exercise_json_content, file, indent = 4)
            file.close()
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
            add_widget(Item(text=exercise.get("exercise").replace('.json', ''), size_hint=(0.2,0.4), pos_hint={'center_y': 0.5, 'center_x': 0.5}))
            current_dir = os.getcwd()
            os.chdir("../..")
            arrow = Image(source = 'graphics/whiteArrow.png', size_hint=(None,None), pos_hint={'center_y': 0.5, 'center_x': 0.5}) 
            add_widget(arrow)
            os.chdir(current_dir)
        self.manager.current = 'edit timeline' 

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

    def update_exercise_json(self):      
        exercise_json_content["keyframes"].append({"points": frame_points,"timeLimit" : self.index_input2.text})
        #print(exercise_json_content)

    def call_pops(self):
        # create content and add to the popup
        self.pop_content = Button(text='')
        popup = Popup(title = "Warning!", content=self.pop_content, size_hint=(0.5,0.2), auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        self.pop_content.bind(on_press=popup.dismiss)

        # open the popup
        popup.open()
    
    def edit(self, instance):
        print("Edit was pressed!")
    
    def delete(self, instance):
        #Instance refers to the Button, while its parent is the BoxLayout within which the Button is contained
        #We need to remove the DraggableItem itself, which is the parent of the BoxLayout
        #We remove this DraggableItem from its parent, that is the ReorderableLayout
        itemToBeRemoved = instance.parent.parent
        layoutToRemoveFrom = itemToBeRemoved.parent
        layoutToRemoveFrom.remove_widget(itemToBeRemoved)