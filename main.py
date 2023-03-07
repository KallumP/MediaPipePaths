from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

import os
#import src.helper
#import src.GestureEditor
#import src.GestureTracker
import src.gui.HomeScreen
import src.gui.SelectTimeline
import src.gui.NewTimeline
import src.gui.EditTimeline
import src.gui.NewExercise
import src.gui.EditExercise
import src.gui.RecordFrame
import src.gui.TestExercise
#from src.gui import  

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("motion-9821b-firebase-adminsdk-3ckyy-d8eb4e8958.json")

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class Application(App):
    def build(self):
        os.chdir('timelines')
        sm = ScreenManagement(transition=FadeTransition())
        sm.add_widget(src.gui.HomeScreen.HomeScreen(name='home'))
        sm.add_widget(src.gui.SelectTimeline.SelectTimeline(name='select timeline'))
        sm.add_widget(src.gui.NewTimeline.NewTimeline(name='new timeline'))
        sm.add_widget(src.gui.EditTimeline.EditTimeline(name='edit timeline'))
        sm.add_widget(src.gui.NewExercise.NewExercise(name='new exercise'))
        sm.add_widget(src.gui.EditExercise.EditExercise(name='edit exercise'))
        sm.add_widget(src.gui.RecordFrame.RecordFrame(name='record frame'))
        sm.add_widget(src.gui.TestExercise.TestExercise(name='test exercise'))
        
        return sm

if __name__ == "__main__":  
    Application().run()