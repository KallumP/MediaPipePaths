from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import cv2
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import mediapipe as mp
from kivy.clock import Clock
import cv2
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

import src.gui.EditExercise
from kivy.core.window import Window

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class RecordFrame(Screen):
    def __init__(self, **kwargs):
        super(RecordFrame, self).__init__(**kwargs) 
        self.layout = BoxLayout(orientation = 'vertical')

        self.texture1 = None

        # this area is used to show gestures catched by camera
        image_area = BoxLayout(size_hint=(1, 0.8))
        self.img1 = Image()
        image_area.add_widget(self.img1)
        #mediaPipe
        self.mp_pose = mp.solutions.pose
        self.pose_model = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # self.update_event = Clock.schedule_interval(self.update, 1.0/3000.0)
        self.update_event = None

        self.layout.add_widget(image_area)

        btn_area = BoxLayout(orientation = 'horizontal', size_hint=(1, None), height=80)
        self.record_btn = Button(text="Record",size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, font_size='25sp', disabled = False)
        self.record_btn.bind(on_press=self.record)
        btn_area.add_widget(self.record_btn)

        self.cancel_btn = Button(text="Cancel",size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, font_size='25sp', disabled = False)
        self.cancel_btn.bind(on_press=self.cancel)
        btn_area.add_widget(self.cancel_btn)
        
        self.confirm_btn = Button(text="Confirm", size_hint=(0.3,1), pos_hint={'center_x': 0.5}, font_size='25sp', disabled = False)
        self.confirm_btn.bind(on_press=self.confirm)
        btn_area.add_widget(self.confirm_btn)

        self.layout.add_widget(btn_area)
        self.add_widget(self.layout)
    
    def start_update(self):
        self.update_event = Clock.schedule_interval(self.update, 1.0/3000.0)

    def confirm(self, instance):
        if self.update_event is not None and self.update_event.is_triggered:
            self.update_event.cancel()

        if self.texture1 is not None:
            self.manager.get_screen('edit exercise').img1.texture = self.texture1
            self.manager.current = 'edit exercise'
        else:
            self.manager.current = 'edit exercise'

    def record(self, instance):
        self.record_btn.disabled = True
        self.cancel_btn.disabled = True
        self.confirm_btn.disabled = True
        if not self.update_event.is_triggered:
            self.update_event = Clock.schedule_interval(self.update, 1.0/3000.0)
        if self.texture1 is not None:
            self.texture1 = None
        self.countdown(5, self.capture_image)

    def capture_image(self):
        self.update_event.cancel()
        self.record_btn.disabled = False
        self.cancel_btn.disabled = False
        self.confirm_btn.disabled = False
        #print(self.results.pose_landmarks)

        src.gui.EditExercise.key_frame_index_result = self.results.pose_landmarks

        ret, capture_frame = self.capture.read()
        capture_frame = cv2.resize(capture_frame, (Window.width, Window.height))
        # Convert the image to a texture and display it in the Image widget
        image = cv2.cvtColor(capture_frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        

        # define the colors for drawing
        landmark_color = (0, 255, 0)  # green color for landmarks
        line_color = (0, 0, 255)  # red color for connections between landmarks
        line_width = 2
        # get the dimensions of the image
        image_height, image_width, _ = image.shape

        # Flip the image horizontally
        image = cv2.flip(image, 1)

        for landmark in self.results.pose_landmarks.landmark:
            # convert landmark from relative coordinates to pixel coordinates
            x = int(landmark.x * image_width)
            y = int(landmark.y * image_height)
            # draw a circle at the landmark point
            cv2.circle(image, (x, y), radius=5, color=landmark_color, thickness=-1)

        # draw connections between landmarks
        for connection in self.mp_pose.POSE_CONNECTIONS:
            start_landmark = self.results.pose_landmarks.landmark[connection[0]]
            end_landmark = self.results.pose_landmarks.landmark[connection[1]]
            # convert landmarks from relative coordinates to pixel coordinates
            start_x, start_y = int(start_landmark.x * image_width), int(start_landmark.y * image_height)
            end_x, end_y = int(end_landmark.x * image_width), int(end_landmark.y * image_height)
            # draw a line between the two landmarks
            cv2.line(image, (start_x, start_y), (end_x, end_y), color=line_color, thickness=line_width)
        
        # Flip the image horizontally
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.flip(image, 1)
        buf1 = cv2.flip(image, 0)
        buf = buf1.tostring()
        self.texture1 = Texture.create(size=(capture_frame.shape[1], capture_frame.shape[0]), colorfmt='bgr')  
        self.texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img1.texture = self.texture1

    def countdown(self, seconds, callback):
        self.countdown_label = Label(text=str(seconds), font_size='100sp', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.countdown_label)
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)
        self.countdown_seconds = seconds
        self.countdown_callback = callback

    def update_countdown(self, dt):
        self.countdown_seconds -= 1
        if self.countdown_seconds == 0:
            self.remove_widget(self.countdown_label)
            self.countdown_event.cancel()
            self.countdown_callback()
        else:
            self.countdown_label.text = str(self.countdown_seconds)

    def cancel(self, instance):
        if self.update_event is not None and self.update_event.is_triggered:
            self.update_event.cancel()
        self.manager.current = 'edit exercise'
        # if self.update_event is not None and self.update_event.is_triggered:
        #     # if update event is not cancelled, then return to edit exercise page
        #     self.manager.current = 'edit exercise'
        # else:
        #     # if update event is cancelled, then start it again
        #     self.update_event = Clock.schedule_interval(self.update, 1.0/3000.0)

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        frame = cv2.resize(frame, (Window.width, Window.height))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        self.results = self.pose_model.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # draws the body
        self.mp_drawing.draw_landmarks(
            image,
            self.results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        image = cv2.flip(image, 1)
        # convert it to texture
        buf1 = cv2.flip(image, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')  
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1
