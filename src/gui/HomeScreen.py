from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window


#Can be changed later depending on the window size required
#1280x720 works well for testing purposes
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        #Window.clearcolor = (1, 1, 1, 1)
        layout = BoxLayout(orientation='vertical', spacing=10)

        padding1 = Label(text='', font_size = '10sp')
        layout.add_widget(padding1)

        title_text = Label(text='Welcome to UCL Exercise Editor', font_size = '50sp', markup=True)
        layout.add_widget(title_text)

        createTimeline_btn = Button(text="Create New Timeline", size_hint=(0.4,0.3), pos_hint={'center_x': 0.5})
        createTimeline_btn.bind(on_press=self.createNewTimeLine)
        layout.add_widget(createTimeline_btn)

        viewTimeline_btn = Button(text="View Timeline", size_hint=(0.4,0.3), pos_hint={'center_x': 0.5})
        viewTimeline_btn.bind(on_press=self.viewTimeline)
        layout.add_widget(viewTimeline_btn)

        viewTimeline_btn = Button(text="New exercise", size_hint=(0.4,0.3), pos_hint={'center_x': 0.5})
        viewTimeline_btn.bind(on_press=self.createNewExercise)
        layout.add_widget(viewTimeline_btn)

        padding2 = Label(text='', font_size = '10sp')
        layout.add_widget(padding2)

        self.add_widget(layout)
        #return layout
    
    def createNewTimeLine(self, instance):
        self.manager.current = 'new timeline'       

    def viewTimeline(self, instance):
        self.manager.current = 'select timeline'    
    
    def createNewExercise(self, instance):
        self.manager.current = 'new exercise'  

if __name__ == '__main__':
    HomeScreen().run()