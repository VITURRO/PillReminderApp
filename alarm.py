from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

class AlarmApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.alarms_screen = Screen(name='alarms_screen')

        # Agregar la imagen de fondo
        background_image = Image(source='fondo2.png', allow_stretch=True, keep_ratio=False)
        self.alarms_screen.add_widget(background_image)

        # Cargar el contenido desde el archivo kv
        Builder.load_string('''
<AlarmsScreen>:
    RelativeLayout:
        Image:
            source: 'fondo2.png'
            allow_stretch: True
            keep_ratio: False
        Button:
            text: "+ Agregar nueva alarma"
            on_press: root.go_to_main_screen()
            size_hint: None, None
            size: 300, 100
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        Button:
            text: "SALIR"
            on_press: app.stop()
            size_hint: None, None
            size: 100, 50
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        ''')

        alarms_screen = AlarmsScreen(name='alarms_screen')
        self.alarms_screen.add_widget(alarms_screen)

        self.screen_manager.add_widget(self.alarms_screen)
        return self.screen_manager

class AlarmsScreen(Screen):
    def go_to_main_screen(self):
        from main import PillReminderApp
        App.get_running_app().stop()  # Detener la app actual
        PillReminderApp().run()

if __name__ == '__main__':
    AlarmApp().run()
