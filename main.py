from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.image import Image

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
#from src.gui import

arrow = Image(source = 'graphics/whiteArrow.png', size_hint=(None,None), pos_hint={'center_y': 0.5, 'center_x': 0.5})   

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
        
        return sm

if __name__ == "__main__":  
    Application().run()