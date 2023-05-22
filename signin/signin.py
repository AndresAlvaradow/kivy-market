from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
Builder.load_file('signin/signin.kv')
from model.operacionesDB import obtener_user
class SigninWindow(BoxLayout):
    def __init__(self, colocar_user_callback, **kwargs):
        super().__init__(*kwargs)
        self.poner_nombre = colocar_user_callback
        
    def verificacion(self, username, password):
        dic_user = obtener_user(username)
        if username =='' and password=='':
            self.ids.singnin_notificacion.text="Falta usuario o Contraseña"
        else:
            if dic_user == -1:
                self.ids.singnin_notificacion.text="El usuario no existe"
            else:
                if dic_user['username'] == username and dic_user['password'] == password:
                    self.ids.username.text =''
                    self.ids.password.text =''
                    self.ids.singnin_notificacion.text=""
                    if dic_user['tipo']=='trabajador':
                        self.parent.parent.current='scrn_ventas'
                        
                    else:
                        self.parent.parent.current='scrn_admin'
                    self.poner_nombre(dic_user)
                else:
                    self.ids.singnin_notificacion.text="Contraseña  incorrecto"
class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__=="__main__":
    SigninApp().run()