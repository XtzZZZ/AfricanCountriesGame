from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return  Button(text="show", on_press=self.anim_btn)

    def anim_btn(self, *args):
        popupWindow = Popup(
            title="Game over",
            content=Label(text="GG"),
            size_hint=(None, None),
            size=(400, 200),
            separator_color=[0, 255 / 255, 210 / 255, .5],
            background_color=[14 / 88, 0, 30 / 88, 1]
        ).open()

if __name__ == "__main__":
    TestApp().run()