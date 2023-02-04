from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

import os
#import src.helper
#import src.GestureEditor
#import src.GestureTracker
import src.gui.SelectTimeline
import src.gui.EditTimeline
#from src.gui import

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class Application(App):
    def build(self):

        sm = ScreenManagement(transition=FadeTransition())
        #sm.add_widget(src.gui.WelcomeScreen(name='Welcome'))
        sm.add_widget(src.gui.SelectTimeline.SelectTimeline(name='select timeline'))
        #sm.add_widget(src.gui.NewTimeline(name='new timeline'))
        sm.add_widget(src.gui.EditTimeline.EditTimeline(name='edit timeline'))
        #sm.add_widget(src.gui.NewExercise(name='new exercise'))
        #sm.add_widget(src.gui.EditExercise(name='edit exercise'))
        #sm.add_widget(src.gui.RecordFrame(name='record frame'))
        return sm

if __name__ == "__main__":  
    Application().run()