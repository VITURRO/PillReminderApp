from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import datetime
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.audio import Sound
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout  
from plyer import notification





class PillReminderApp(App):
    
        
    def build(self):
        self.layout = RelativeLayout()
        self.sound = SoundLoader.load("alarma.mp3")

        # Agregar la imagen de fondo
        self.background_image = Image(source='fondo1.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background_image)

        # Agregar tus widgets de entrada y otros encima de la imagen de fondo
        self.nombre_pastilla_input = TextInput(hint_text="Nombre de la pastilla", opacity=0.8, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.dosis_input = TextInput(hint_text="Dosis", opacity=0.8, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.hora_input = TextInput(hint_text="Hora (0-23)", opacity=0.8, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.minutos_input = TextInput(hint_text="Minutos (0-59)", opacity=0.8, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})

        self.programar_alarma_button = Button(text="Programar alarma", on_press=self.programar_alarma, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.mensaje_label = Label(text="", opacity=0.8, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2})

        # Agregar los widgets encima de la imagen de fondo
        self.layout.add_widget(self.nombre_pastilla_input)
        self.layout.add_widget(self.dosis_input)
        self.layout.add_widget(self.hora_input)
        self.layout.add_widget(self.minutos_input)
        self.layout.add_widget(self.programar_alarma_button)
        self.layout.add_widget(self.mensaje_label)
        
 # Botón "Volver"
        volver_button = Button(text="Volver", size_hint=(None, None), size=(100, 50), pos_hint={'right': 1, 'bottom': 1})
        volver_button.bind(on_press=self.ir_a_alarm)
        self.layout.add_widget(volver_button)

        # Inicializar la variable para la alarma programada
        self.hora_programada = -1
        self.minutos_programados = -1
        
        return self.layout

    def programar_alarma(self, instance):
        
        nombre_pastilla = self.nombre_pastilla_input.text 
        dosis = self.dosis_input.text
        hora = self.hora_input.text
        minutos = self.minutos_input.text

        # Verificar que la entrada sea válida (números y dentro del rango)
        if not hora.isdigit() or not minutos.isdigit() or int(hora) < 0 or int(hora) > 23 or int(minutos) < 0 or int(minutos) > 59:
            self.mensaje_label.text = "Ingrese una hora y minutos válidos."
            return

        # Almacenar la hora programada
        self.hora_programada = int(hora)
        self.minutos_programados = int(minutos)

        self.mensaje_label.text = f"Alarma programada para tomar la pastilla '{nombre_pastilla}' a las {hora}:{minutos}"
        
        self.apagar_alarma_button = Button(text="Apagar alarma", on_press=self.apagar_alarma, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        self.layout.add_widget(self.apagar_alarma_button)
        
        self.sound_playing = False  # Variable para rastrear si el sonido está reproduciéndose

        Clock.schedule_interval(self.verificar_alarma, 60)  # Verificar cada minuto

    def verificar_alarma(self, dt):
        hora_actual = datetime.datetime.now().hour
        minutos_actual = datetime.datetime.now().minute

        
        if self.hora_programada == hora_actual and self.minutos_programados == minutos_actual:
            self.mostrar_ventana_emergente()
            if not self.sound_playing:
                self.sound.play()  # Reproducir el sonido si no se está reproduciendo
                self.enviar_notificacion()
                
                
    def apagar_alarma(self, instance):
        if self.sound_playing:
            self.sound.stop()  # Detener el sonido
            self.sound_playing = False


    def mostrar_ventana_emergente(self):
        nombre_pastilla = self.nombre_pastilla_input.text
        dosis = self.dosis_input.text
        mensaje = f"Es hora de tomar la pastilla '{nombre_pastilla}'\nDosis: {dosis}"

        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text=mensaje))

        self.apagar_alarma_button = Button(text="Apagar alarma", on_press=self.apagar_alarma, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        content.add_widget(self.apagar_alarma_button)

        self.sound_playing = True

        popup = Popup(title="¡Alarma!", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()
        
        # Reproducir el sonido en bucle cada 2 segundos durante 1 minuto (30 repeticiones)
        if self.sound:
            self.sound.loop = True
            self.sound.play()
            Clock.schedule_once(lambda dt: self.sound.stop(), 60)  # Detener el sonido después de 1 minuto
            
    def enviar_notificacion(self):
        nombre_pastilla = self.nombre_pastilla_input.text
        dosis = self.dosis_input.text

        mensaje = f"Es hora de tomar la pastilla '{nombre_pastilla}'\nDosis: {dosis}"

        notification_title = "¡Recordatorio de Pastilla!"
        notification_text = mensaje

        notification.notify(
            title=notification_title,
            message=notification_text,
            app_name="Pill Reminder App",
            timeout=120 # Duración de la notificación en segundos
        )


    def ir_a_alarm(self, instance):
        from alarm import AlarmApp
        self.stop()  # Detener la app actual
        self.sound.stop()  # Detener el sonido antes de cambiar de pantalla
        AlarmApp().run()


if __name__ == '__main__':
    PillReminderApp().run()