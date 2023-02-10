'''
When you want to make ``StackLayout`` re-orderable, you may want to disable
the ``size_hint`` of each child, or may want to limit the maximum size of
each child, otherwise the layout may be messed up. You can confirm it by
commenting/uncommenting the ``TestApp.on_start()``'s body.
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.app import App
import kivy_garden.draggable


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


def random_size():
    from random import uniform
    return (uniform(50.0, 150.0), uniform(50.0, 150.0), )


class TestApp(App):
    def build(self):
        return Builder.load_string(KV_CODE)

    def on_start(self):
        Item = Factory.MyDraggableItem
        Item()
        add_widget = self.root.ids.layout.add_widget
        for i in range(30):
            # A (works)
            add_widget(Item(text=str(i), size=random_size(), size_hint=(None, None)))

            # B (works)
            # add_widget(Item(text=str(i), size_hint_max=random_size()))

            # C (does not work)
            # add_widget(Item(text=str(i), size_hint_min=random_size()))

            # D (does not work)
            # add_widget(Item(text=str(i)))


if __name__ == '__main__':
    TestApp().run()