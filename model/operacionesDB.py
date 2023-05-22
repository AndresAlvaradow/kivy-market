from .conexion import ConexionBD
def obtener_producto():
    conec = ConexionBD()
    lista_productos=[]
    sql= "SELECT * FROM productos"
    conec.cursor.execute(sql)
    lista_productos = conec.cursor.fetchall()
    conec.conexion.close()
    lista_data =[]
    for producto in lista_productos:
        dic = {'codigo': producto[0],'tipo':producto[1] ,'nombre': producto[2],'cantidad':producto[3] ,'precio_c': producto[4], 'precio':producto[5]}
        lista_data.append(dic)
    return lista_data
def obtener_user(nameuser):
    conec = ConexionBD()
    lista_user=[]
    sql= f"SELECT * FROM usuarios WHERE nameuser ='{nameuser}'"
    conec.cursor.execute(sql)
    lista_user= conec.cursor.fetchall()
    conec.conexion.close()
    dic_user={}
    for user in lista_user:
        dic_user={'name': user[1], 'username': user[2], 'password': user[3], 'tipo': user[4]}
    if dic_user !={}:
        
        return dic_user
    else:
        dic_user = -1
        return dic_user
def actualizar_cantidad(codigo, new_cantidad):
    conec = ConexionBD()
    sql_cantidad = f"UPDATE productos SET cantidad = '{new_cantidad}' WHERE (codigo = '{codigo}')"
    conec.cursor.execute(sql_cantidad)
    conec.conexion.commit()
    conec.conexion.close()

def insertar_producto(tuple_producto):
    conec = ConexionBD()
    sql ="""INSERT INTO productos (codigo,tipo, nombre, cantidad, pcompra, pvp) VALUES (%s, %s, %s, %s, %s,%s)"""
    conec.cursor.execute(sql, tuple_producto)
    conec.conexion.commit()
    conec.conexion.close()

def actualizar_producto(producto):
    conec = ConexionBD()
    sql_update =f"""UPDATE productos set tipo = '{producto['tipo']}',nombre = '{producto['nombre']}', cantidad = '{producto['cantidad']}', pcompra = '{producto['precio_c']}', pvp = '{producto['precio']}' 
    WHERE (codigo = '{producto['codigo']}')"""
    conec.cursor.execute(sql_update)
    conec.conexion.commit()
    conec.conexion.close()

def eliminar_producto(codigo):
    conec = ConexionBD()
    sql_del =f"""DELETE FROM productos WHERE codigo = '{codigo}'"""
    conec.cursor.execute(sql_del)
    conec.conexion.commit()
    conec.conexion.close()


def obtener_usuarios():
    conec = ConexionBD()
    lista_users=[]
    sql= f"SELECT * FROM usuarios"
    conec.cursor.execute(sql)
    lista_users= conec.cursor.fetchall()
    conec.conexion.close()
    lista_data=[]
    dic_user={}
    for user in lista_users:
        dic_user={'id_user':user[0] ,'nombre': user[1], 'username': user[2], 'password': user[3], 'tipo': user[4]}
        lista_data.append(dic_user)
    if lista_data !=[]:   
        return lista_data
    else:
        lista_data = -1
        return lista_data

def agregar_usuario(tupla_user):
    conec = ConexionBD()
    sql_insert = "INSERT INTO usuarios (idusuarios, nombre, nameuser, password, tipo) VALUES (%s, %s,%s,%s,%s)"
    conec.cursor.execute(sql_insert, tupla_user)
    conec.conexion.commit()
    conec.conexion.close()

def actualizar_user(user):
    conec = ConexionBD()
    sql_update = f"""UPDATE usuarios SET nombre = '{user['nombre']}', nameuser = '{user['username']}', password = '{user['password']}', tipo= '{user['tipo']}' 
    WHERE (idusuarios = '{user['id_user']}')"""
    conec.cursor.execute(sql_update)
    conec.conexion.commit()
    conec.conexion.close()

def eliminar_user(id_user):
    conec = ConexionBD()
    sql_del = f"DELETE FROM usuarios WHERE idusuarios = '{id_user}'"
    conec.cursor.execute(sql_del)
    conec.conexion.commit()
    conec.conexion.close()