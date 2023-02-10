from kivy.lang import Builder
from kivy.factory import Factory
from kivy.app import App
import kivy_garden.draggable
from kivy.uix.button import Button

KV_CODE = '''
<MyReorderableLayout@KXReorderableBehavior+StackLayout>:
    spacing: 10
    padding: 10
    cols: 4
    drag_classes: ['test', ]
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
ScrollView:
    MyReorderableLayout:
        id: layout
        size_hint_min: self.minimum_size
'''

#Constant Variables
WIDTH = 100
HEIGHT = 50

#List for Testing - To remove and replace with Json list
pyList = ['2', '3', '4', '5', '6']

class EditTimeline(App):
    def  build(self):
        return Builder.load_string(KV_CODE)

    def on_start(self):
        #Print statement - Debugging Purposes Only
        Item = Factory.MyDraggableItem
        Item()
        add_widget = self.root.ids.layout.add_widget

        #Replace with Json list
        for i in pyList:
            add_widget(Item(text=str(i), size=(WIDTH, HEIGHT), size_hint=(None,None)))

        saveButton = Button(text="Save Timeline", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5})
        saveButton.bind(on_press=self.saveTimeline)
        add_widget(saveButton)
    
    def saveTimeline(self, instance):
        updatedList=[]
        for widget in self.root.ids.layout.children:
            #Check if widget is of type draggable item and insert into list if true
            #Important to insert at index 0, and not append, as layouts have a stack-like structure
            if(str(type(widget))=="<class 'kivy.factory.MyDraggableItem'>"):
                updatedList.insert(0, widget.text)
        #Print the Updated List for Now, Can return list if needed
        print(updatedList)
        

if __name__ == '__main__':
    EditTimeline().run()