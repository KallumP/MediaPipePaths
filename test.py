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
from kivy.app import App

from kivy.graphics import Ellipse, Color, Line, Rectangle, Triangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
      
class ScrollTest(ScrollView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    
        Window.bind(on_maximize=self.testing)
        
        self.size_hint = (1,None)
        self.pos_hint = {'center_x':0.5,'top': 1}
        self.size = (Window.width,Window.height)

        self.inside = GridLayout()
        self.inside.cols = 1
        self.inside.size_hint_y= None
        self.inside.spacing = 10
        
        self.inside.bind(minimum_height=self.inside.setter('height'))#checks when window maximized
        
        for i in range(1,5):
            self.submit = Button(text='something',size_hint_y=None, height=40)
            self.submit.bind(on_press=self.wPressed)
            self.inside.add_widget(self.submit)
        
        self.add_widget(self.inside)
        
    def wPressed(self,instance):
        self.submit = Button(text='something',size_hint_y=None, height=40)
        self.submit.bind(on_press=self.wPressed)
        self.inside.add_widget(self.submit)
            
    def testing(self,instance):
        self.size= (Window.width,Window.height)

        
class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        '''Creation of login screen'''
        self.login_page = ScrollTest()
        screen = Screen(name= 'Login')
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager


if __name__ == '__main__':
    MyApp().run()