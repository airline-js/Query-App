from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import requests


class LoginPage(MDApp):

    def build(self):
        global screen_manager
        self.theme_cls.primary_palette = 'Gray'
        self.theme_cls.theme_style = "Dark"
        Clock.schedule_interval(self.on_start, 0.1)
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('pre-splash.kv'))
        screen_manager.add_widget(Builder.load_file('login.kv'))
        return screen_manager

    def on_start(self, *args):
        try:
            progress_value = 1
            screen_manager.current_screen.ids.progress.value += progress_value
            if screen_manager.current_screen.ids.progress.value == 100:
                self.change_screen()
        except:
            Clock.unschedule(self.on_start)

    def change_screen(self):
        screen_manager.current = "login"

    def search_query(self):
        user_query = screen_manager.current_screen.ids.rounded_button.text
        try:
            request = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{user_query}")
            query_meaning = request.json()[0]['meanings'][0]['definitions'][0]['definition']

        except:
            self.query_dialog = MDDialog(title="Not Found", text="Try something else",
                                         buttons=[
                                             MDFlatButton(
                                                 text="CLOSE",
                                                 theme_text_color="Custom",
                                                 text_color=self.theme_cls.primary_color,
                                                 on_release=self.closeDialog
                                             )
                                         ], radius=[20, 7, 20, 7]
                                         )
        else:
            self.query_dialog = MDDialog(title=user_query, text=query_meaning,
                                         buttons=[
                                             MDFlatButton(
                                                 text="CLOSE",
                                                 theme_text_color="Custom",
                                                 text_color=self.theme_cls.primary_color,
                                                 on_release=self.closeDialog
                                             )
                                         ], radius=[20, 7, 20, 7]
                                         )
        finally:
            self.query_dialog.open()

    def closeDialog(self, inst):
        self.query_dialog.dismiss()


if __name__ == '__main__':
    LoginPage().run()
