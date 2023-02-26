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
from kivy.graphics import Ellipse, Color, Line, Rectangle, Triangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class EditExercise(Screen):
    def __init__(self, **kwargs):

        super(EditExercise, self).__init__(**kwargs) 

        self.exercise_name = "punch"
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
        top_area.add_widget(Label(text=self.exercise_name, 
                                  font_size='30sp'))
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
        dropdown = DropDown()
        typeList = ['triPointAngle', 'None', 'pointPosition', 'parallelPosition', 'abovePosition']
        for index in range(len(typeList)):
            btn = Button(text=typeList[index], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        self.mainbutton = Button(text='Click to Choose Type')
        pointtype.add_widget(self.mainbutton)
        self.mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))

        leniency = BoxLayout(orientation='vertical')
        select_box.add_widget(leniency)
        leniency.add_widget(Label(text='Leniency',
                              font_size='15sp'))
        self.leniency_value = Label(text='0.0', font_size='15sp')
        leniency.add_widget(self.leniency_value)
        self.slider = Slider(min=0, max=2, value=0)
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
        

    def setter(self, window, width, height):
        self.root.width = width
        self.root.height = height

    def record_frame(self, instance):
        self.manager.current = 'record frame'
        
    def move_slider(self, *args):
        self.leniency_value.text = str(round(self.slider.value, 2))

    def ok(self, instance):
        # indexes
        print(self.index_input1.text)
        # time limit
        print(self.index_input2.text)
        # point type
        print(self.mainbutton.text)
        # leniency
        print(round(self.slider.value, 2))
    
    def reset(self, instance):
        return 1
    
    def next(self, instance):
        return 1

    def complete(self, instance):
        return 1

    def cancel(self, instance):
        self.manager.current = 'home'
    
    def refresh(self):
        self.name_label.text = self.exercise_name

    def update_exercise_json(self):
        
        with open(self.name_label.text + ".json",'r+') as file:
          # First we load existing data into a dict.
            exercise_data = json.load(file)
            
            # python object to be appended
            #new_keyframe = {"exercise": self.exercise_name.text+".json"}
            
            # appending the data
            #timeline_data["keyframes"].append(new_keyframe)
            
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(exercise_data, file, indent = 4)