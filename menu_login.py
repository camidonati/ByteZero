import sys
import BBDD
import web_scraping as WS
import CRUD 

def cargar_usuario():
    # Iniciamos la base de datos
    conexion = BBDD.abrir_base()
    cursor = conexion.cursor()

    while True:
        print("-" * 90)
        nombre_del_usuario = input("Ingrese un nombre de usuario: ")
        # Ver si el usuario es único
        consulta = "SELECT usuario FROM usuarios WHERE usuario = %s"
        valor = (nombre_del_usuario,)
        cursor.execute(consulta, valor)
        resultado_consulta = cursor.fetchone()
        if resultado_consulta is None:
            print("Este usuario no existe, puede continuar")
            break
        else:
            print("Este usuario ya existe, intente nuevamente")

    while True:
        contrasena = input("Ingrese una contraseña: ")
        repetir_contrasena = input("Repita la contraseña: ")
        if contrasena == repetir_contrasena:
            break
        else:
            print("Las contraseñas deben coincidir")
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")

    # Consulta SQL para insertar datos en la tabla "usuarios"
    consulta_usuarios = "INSERT INTO usuarios (usuario, contraseña, nombre, apellido) VALUES (%s, %s, %s, %s)"
    valores_usuarios = (nombre_del_usuario, contrasena, nombre, apellido)

    # Ejecutar la consulta de inserción
    cursor.execute(consulta_usuarios, valores_usuarios)

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar la conexión a la base de datos
    conexion.close()

    print("Usuario registrado exitosamente")
    menu_datos ()

def inicio_usuario():
    contador = 0

    # Iniciamos la base de datos
    conexion = BBDD.abrir_base()
    cursor = conexion.cursor()

    while True:
        print("-" * 90)
        usuario_registrado = input("Ingrese su usuario: ")
        contrasena = input("Ingrese la contraseña: ")

        # Consultar la base de datos para verificar las credenciales
        consulta = "SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s"
        valores = (usuario_registrado, contrasena)
        cursor.execute(consulta, valores)
        resultado_consulta_usuario = cursor.fetchone()

        if resultado_consulta_usuario is None:
            print("Usuario o contraseña incorrectos. Inténtalo de nuevo.")
            contador += 1
        else:
            print("-" * 90)
            print("Inicio de sesión exitoso. Bienvenido,", resultado_consulta_usuario[3], resultado_consulta_usuario[4] )
            print("-" * 90)
            # Cerrar la conexión a la base de datos
            conexion.close()
            menu_datos ()

        if contador == 3:
            print("-" * 90)
            print("Límites de intentos superados")
            print("-" * 90)
            # Cerrar la conexión a la base de datos
            conexion.close()
            sys.exit()

def menu_datos ():
    
    
    while True:
            print("-" * 90)
            print("¿Que datos desea consultar?")
            print("-" * 90)
            print("1. Emigracion")
            print("2. Inmigracion")
            print("0. Salir")
            opcion = int(input("Ingrese una opcion: "))
            if (opcion >= 0 and opcion <= 2):
                if opcion == 1:
                    datos = "emigracion"
                    menu_usuario (datos)
                    
                
                elif opcion == 2:
                    datos = "inmigracion"
                    menu_usuario (datos)
                    

                elif opcion == 0:
                    sys.exit()
                    
            else:
                print("Opcion incorrecta, intente de nuevo")

def menu_usuario(datos):
    print("-" * 90)
    print ("Espere por favor mientras procesamos los datos.")
    print("-" * 90)
    WS.web_scraping (datos)
    while True:
        print("-" * 90)
        print("Menú de usuario:")
        print("-" * 90)
        print("1. Consultar registro por Id")
        print("2. Agregar registro a la base")
        print("3. Modificar registro por Id")
        print("4. Eliminar registro por Id")
        print("5. Imprmir base de datos actualizada")
        print("0. Volver")
        print("-" * 90)
        
        opcion = int(input("Ingrese una opcion: "))
        if (opcion >= 0 and opcion <= 5):
                if opcion == 1:
                    CRUD.consulta_por_id(datos)
                    
                
                elif opcion == 2:
                    datos = "inmigracion"
                    menu_usuario (datos)
                    
                
                elif opcion == 3:
                    datos = "inmigracion"
                    menu_usuario (datos)
                    
                
                elif opcion == 4:
                    datos = "inmigracion"
                    menu_usuario (datos)
                    
                
                elif opcion == 5:
                    datos = "inmigracion"
                    menu_usuario (datos)
                    

                elif opcion == 0:
                    break
                    
        else:
                print("Opcion incorrecta, intente de nuevo")
    

# menu inicial
print("-" * 90)
print ("Bienvenidos al sistema de consulta ByteZero")
print("-" * 90)
while True:
            print ("1- Iniciar sesion \n2- Registrarse \n0- Salir")
            print("-" * 90)
            opcion = int(input("Ingrese una opcion: "))
            if (opcion >= 0 and opcion <= 2):
                if opcion == 1:
                    inicio_usuario()
                    
                elif opcion == 2:
                    cargar_usuario()

                elif opcion == 0:
                    sys.exit()
                    
            else:
                print("Opcion incorrecta, intente de nuevo")

