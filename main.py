from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from signin.signin import SigninWindow
from admin.admin import AdminWindow
from ventas.ventas import VentasWindows
from model.operacionesDB import obtener_user
class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.ventas_widget = VentasWindows()
        self.signin_widget = SigninWindow(self.ventas_widget.colocar_user)
        self.admin_widget = AdminWindow()
        self.ids.scrn_signin.add_widget(self.signin_widget)
        self.ids.scrn_ventas.add_widget(self.ventas_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget )


class MainApp(App):
    def build(self):
        return MainWindow()

if __name__=="__main__":
    MainApp().run()
    obtener_user('admin')