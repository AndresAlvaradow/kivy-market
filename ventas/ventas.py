from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.clock import Clock
from datetime import datetime, timedelta
import sys
sys.path.append(r"C:\\python\\xavier\\market_kivy")
from model.operacionesDB import obtener_producto, actualizar_cantidad
from kivy.lang import Builder
Builder.load_file('ventas/ventas.kv')
'''inventario=[
    {'codigo': '111','tipo':'Lacteos' ,'nombre': 'leche 1L','precio_c':0.90 ,'precio': 1.30, 'cantidad': 20},
    {'codigo': '222', 'tipo':'cereales' ,'nombre': 'cereal 500g','precio_c':0.85 , 'precio': 1.5, 'cantidad': 15}, 
    {'codigo': '333','tipo':'Lacteos' , 'nombre': 'yogurt 1L','precio_c':2.00 , 'precio': 2.50, 'cantidad': 10},
    {'codigo': '444','tipo':'frios' , 'nombre': 'helado 2L','precio_c':0.50 , 'precio': 0.80, 'cantidad': 20},
    {'codigo': '555','tipo':'mascota' , 'nombre': 'alimento para perro 20kg','precio_c':2.30 , 'precio': 2.50, 'cantidad': 5},
    {'codigo': '666', 'tipo':'belleza' ,'nombre': 'shampoo','precio_c':4.50 , 'precio': 5.00, 'cantidad': 25},
    {'codigo': '777','tipo':'personal' , 'nombre': 'papel higiénico 4 rollos','precio_c':1.15 , 'precio': 1.25, 'cantidad': 30},
    {'codigo': '888', 'tipo':'limpieza' ,'nombre': 'jabón para trastes','precio_c':0.90 , 'precio': 1.00, 'cantidad': 5},
    {'codigo': '999', 'tipo':'bebidas' ,'nombre': 'refresco 600ml', 'precio_c':0.40 ,'precio': 0.60, 'cantidad': 10},
    {'codigo': '123','tipo':'Lacteos' ,'nombre': 'leche nutri','precio_c':0.90 ,'precio': 1.30, 'cantidad': 20}
]'''
inventario = obtener_producto()
#codigo, tipo, nombre, cantidad, pcompra, pvp
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True)

class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids['_codigo'].text = str(1+index)
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad_carrito'])
        self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))
        self.ids['_precio'].text = str("{:.2f}".format(data['precio_total']))

        return super(SelectableBoxLayout, self).refresh_view_attrs(
        rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            #print("selection changed to {0} y {1}".format(rv.data[index], 22))
            rv.data[index]['seleccionado']=True
        else:
            #print("selection removed for {0}".format(rv.data[index]))
            rv.data[index]['seleccionado']=False

class SelectableBoxLayoutPopup(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids['_codigo'].text = data['codigo']
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio'].text = str("{:.2f}".format(data['precio']))

        return super(SelectableBoxLayoutPopup, self).refresh_view_attrs(
        rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayoutPopup, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            #print("selection changed to {0} y {1}".format(rv.data[index], 22))
            rv.data[index]['seleccionado']=True
        else:
            #print("selection removed for {0}".format(rv.data[index]))
            rv.data[index]['seleccionado']=False

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.modificar_producto = None
    def agregar_articulo(self, articulo):
        articulo['seleccionado'] = False
        indice = -1
        if self.data:
            for i in range(len(self.data)):
                if articulo['codigo']== self.data[i]['codigo']:
                    indice = i
            if indice >=0:
                self.data[indice]['cantidad_carrito']+=1
                self.data[indice]['precio_total'] = self.data[indice]['precio']*self.data[indice]['cantidad_carrito']
                self.refresh_from_data()
            else:
                self.data.append(articulo)
        else:
            self.data.append(articulo)
    def eliminar_articulo(self):
        indice = self.articulo_seleccionado()
        precio=0
        if indice>=0:
            self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            precio=self.data[indice]['precio_total']
            self.data.pop(indice)
            self.refresh_from_data()
        return precio
    def modificar_articulo(self):
        indice = self.articulo_seleccionado()
        if indice>=0:
            popup = CambiarCantidadPopup(self.data[indice], self.actualizar_articulo)
            popup.open()
    def actualizar_articulo(self, valor):
        indice = self.articulo_seleccionado()
        if indice>=0:
            if valor==0:
                self.data.pop(indice)
                self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            else:
                self.data[indice]['cantidad_carrito'] = valor
                self.data[indice]['precio_total'] = self.data[indice]['precio']*valor
            self.refresh_from_data()
            nuevo_total=0
            for data in self.data:
                nuevo_total +=data['precio_total']
            self.modificar_producto(False, nuevo_total)

    def articulo_seleccionado(self):
        indice =-1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice = i
                break
        return indice
class ProductoPorNombrePopup(Popup):
    def __init__(self,input_nombre, agregar_producto_callbalck, **kwargs):
        super(ProductoPorNombrePopup, self).__init__(**kwargs)
        self.input_nombre = input_nombre
        self.agregar_producto=agregar_producto_callbalck

    def mostrar_articulos(self):
        self.open()
        for nombre in inventario:
            if nombre['nombre'].lower().find(self.input_nombre)>=0:
                producto={'codigo':nombre['codigo'],'nombre':nombre['nombre'], 'precio':nombre['precio'], 'cantidad':nombre['cantidad']}
                self.ids.rvs.agregar_articulo(producto)
    def seleccionar_articulo(self):
        indice = self.ids.rvs.articulo_seleccionado()
        if indice >=0:
            _articulo= self.ids.rvs.data[indice]
            articulo={}
            articulo['codigo'] = _articulo['codigo']
            articulo['nombre'] = _articulo['nombre']
            articulo['precio'] = _articulo['precio']
            articulo['cantidad_carrito'] = 1
            articulo['cantidad_inventario'] = _articulo['cantidad']
            articulo['precio_total'] = _articulo['precio']
            if callable(self.agregar_producto):
                self.agregar_producto(articulo)
            self.dismiss()
        
class CambiarCantidadPopup(Popup):
    def __init__(self, data,actualizar_articulo_callback, **kwargs):
        super(CambiarCantidadPopup, self).__init__(**kwargs)
        self.data = data
        self.actualizar_articulo = actualizar_articulo_callback
        self.ids.info_nueva_cant_1.text = "Producto: "+ self.data['nombre'].capitalize()
        self.ids.info_nueva_cant_2.text = "Cantidad: "+ str(self.data['cantidad_carrito'])
    
    def validar_input(self, texto_input):
        try:
            nueva_cantidad = int(texto_input)
            self.ids.notificacion_no_valido.text =''
            self.actualizar_articulo(nueva_cantidad)
            self.dismiss()
        except:
            self.ids.notificacion_no_valido.text ='Cantidad no valida'
class PagarPopup(Popup):
    def __init__(self, total, pago_callback ,**kwargs):
        super(PagarPopup, self).__init__(**kwargs)
        self.total = total
        self.pagado = pago_callback
        self.ids.total.text ="{:.2f}".format(self.total)
    def mostrar_cambio(self):
        recibido = self.ids.recibido.text
        try:
            cambio = float(recibido)- float(self.total)
            if cambio>=0:
                self.ids.cambio.text="{:.2f}".format(cambio)
                self.ids.boton_pagar.disabled = False
            else:
                self.ids.cambio.text="Cambio es menor a la cantidad ingresada"
        except:
            self.ids.cambio.text= "Pago no valido"
    def terminar_pago(self):
        self.pagado()
        self.dismiss()

class NuevaCompraPopup(Popup):
    def __init__(self, nueva_compra_callback ,**kwargs):
        super(NuevaCompraPopup, self).__init__(**kwargs)
        self.nueva_compra = nueva_compra_callback
        self.ids.aceptar.bind(on_release=self.dismiss)

class VentasWindows(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0.0
        self.ids.rvs.modificar_producto= self.modificar_producto

        self.ahora = datetime.now()
        self.ids.fecha.text = self.ahora.strftime("%d/%m%y")
        Clock.schedule_interval(self.actualizar_hora, 1)

    def actualizar_hora(self, *args):
        self.ahora = self.ahora+timedelta(seconds=1)
        self.ids.hora.text = self.ahora.strftime("%H:%M:%S")

    def agregar_producto(self, articulo):
        self.total+= float(articulo['precio'])
        self.ids.sub_total.text = '$ '+"{:.2f}".format(self.total)
        self.ids.rvs.agregar_articulo(articulo)

    def agregar_producto_codigo(self, codigo):
        for producto in inventario:
            if codigo == producto['codigo']:
                articulo={}
                articulo['codigo']= producto['codigo']
                articulo['nombre']= producto['nombre']
                articulo['precio']= producto['precio']
                articulo['cantidad_carrito']=1
                articulo['cantidad_inventario'] = producto['cantidad']
                articulo['precio_total'] = producto['precio']
                self.agregar_producto(articulo)
                self.ids.buscar_codigo.text =''
                break

    def agregar_producto_nombre(self, nombre):
        self.ids.buscar_nombre.text=''
        popup=ProductoPorNombrePopup(nombre, self.agregar_producto)
        popup.mostrar_articulos()

    def eliminar_producto(self):
        menos_precio = self.ids.rvs.eliminar_articulo()
        self.total  -=menos_precio
        self.ids.sub_total.text = '$ '+"{:.2f}".format(self.total)

    def modificar_producto(self, cambio= True, nuevo_total=None):
        if cambio:
            self.ids.rvs.modificar_articulo()
        else:
            self.total = nuevo_total
            self.ids.sub_total.text = '$ '+"{:.2f}".format(self.total)
    def pagar(self):
        if self.ids.rvs.data:
            popup = PagarPopup(self.total, self.pago)
            popup.open()
        else:
            self.ids.notificacion_falla.text='No existen elementos a pagar'

    def pago(self):
        self.ids.notificacion_exito.text = 'Compra realizada con exito'
        self.ids.notificacion_falla.text=''
        self.ids.total.text="{:.2f}".format(self.total)
        self.ids.buscar_codigo.disabled=True
        self.ids.buscar_nombre.disabled=True
        self.ids.pagar.disabled =True
        nueva_cantidad = []
        for producto in self.ids.rvs.data:
            
            cantidad = producto['cantidad_inventario']-producto['cantidad_carrito']
            if cantidad >=0:
                nueva_cantidad.append({'codigo':producto['codigo'], 'cantidad':cantidad})
            else:
                nueva_cantidad.append({'codigo':producto['codigo'], 'cantidad':0})
        for cantidad in nueva_cantidad:
            res = next((producto for producto in inventario if producto['codigo']==cantidad['codigo']), None)
            res['cantidad']= cantidad['cantidad']
        #print("cantidad nueva", cantidad['codigo'], cantidad['cantidad'])
        actualizar_cantidad(cantidad['codigo'], cantidad['cantidad'])
       
    def nueva_compra(self, desde_popup=False):
        if desde_popup:
            self.ids.rvs.data=[]
            self.total = 0.0
            self.ids.sub_total.text = '0.0'
            self.ids.total.text = '0.0'
            self.ids.notificacion_exito.text = ''
            self.ids.notificacion_falla.text=''
            self.ids.buscar_codigo.disabled=False
            self.ids.buscar_nombre.disabled=False
            self.ids.pagar.disabled = False
            self.ids.rvs.refresh_from_data()
        elif len(self.ids.rvs.data):
            popup = NuevaCompraPopup(self.nueva_compra)
            popup.open()
    def colocar_user(self,user):
        self.ids.bienvenido_label.text = 'Bienvenido: '+ user['name']
        if user['tipo'] == 'trabajador':
            self.ids.admin_boton.disabled=True
        else:
            self.ids.admin_boton.disabled=False
    def admin(self):
        #print(inventario)
        #print("administrador")
        self.parent.parent.current='scrn_admin'

    def signout(self):
        #print("salir")
        self.parent.parent.current='scrn_signin'

    
class VentasApp(App):
    def build(self):
        return VentasWindows()

if __name__ == '__main__':
    VentasApp().run()