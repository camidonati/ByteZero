import BBDD
import tabulate

def consulta_por_id (datos):
    # Iniciamos la base de datos
    conexion = BBDD.abrir_base()
    cursor = conexion.cursor()
    print("Conexión exitosa")
    if datos == "inmigracion":
        # Consulta registro por ID
        consulta_id = int(input("Ingresa el ID del registro que deseas consultar: "))
        cursor.execute("SELECT * FROM inmigracion WHERE id = %s", (consulta_id,))
        res = cursor.fetchall()
        if res is not None:
            imprimir(res, datos)
        
        #Cerramos la base de datos
        conexion.close()
        
    elif datos == "emigracion":
        # Consulta registro por ID
        consulta_id = int(input("Ingresa el ID del registro que deseas consultar: "))
        cursor.execute("SELECT * FROM emigracion WHERE id = %s", (consulta_id,))
        res = cursor.fetchall()
        if res is not None:
            imprimir(res, datos)
        
        #Cerramos la base de datos
        conexion.close()
        
def agregar_registro(datos):
        # Iniciamos la base de datos
        conexion = BBDD.abrir_base()
        cursor = conexion.cursor()
    # Agrega registro por ID        
        anio_nuevo = int(input("Ingresa el nuevo año: "))
        datos_h = int(input("Ingresa la cantidad de " + datos + " de hombres: "))
        datos_w = int(input("Ingresa la cantidad de " +datos +" de mujeres: "))

        if datos == "inmigracion":
            insert_query = """
            INSERT INTO inmigracion (year, inmigration_men, inmigration_women, total_inmigration)
            VALUES (%s, %s, %s, %s)
            """
        elif datos == "emigracion":
            insert_query = """
            INSERT INTO emigracion (year, emigration_men, emigration_women, total_emigration)
            VALUES (%s, %s, %s, %s)
            """
            
        # Calcular el valor de total_inmigration
        total_inmigration = datos_h + datos_w

        data = (
        
            anio_nuevo,
            datos_h,
            datos_w,
            total_inmigration,
        )

        try:
            cursor.execute(insert_query, data)
            conexion.commit()
            cursor.fetchall()
            print("Registro agregado correctamente.")
        except Exception as ex:
            print("Error al agregar el registro:", ex)
            
        
        
def tabla_completa(datos):
    # Iniciamos la base de datos
    conexion = BBDD.abrir_base()
    cursor = conexion.cursor()
    print("Conexión exitosa")
    if datos == "inmigracion":
        # Consulta la tabla imigracion
        cursor.execute("SELECT * FROM inmigracion")
        res = cursor.fetchall()
        imprimir(res,datos)
        #Cerramos la base de datos
        conexion.close()
        
    elif datos == "emigracion":
        # Consulta la tabla emigracion
        cursor.execute("SELECT * FROM emigracion" )
        res = cursor.fetchall()
        imprimir(res,datos)
        #Cerramos la base de datos
        conexion.close()
        
def imprimir(res,datos):
        if res:
            datos = datos.capitalize()
            # Formatear el resultado en una tabla tabulada
            column_names = ["Id", "Año", datos + " Hombres", datos + " Mujeres", "Total " + datos ]
            data = []
            for row in res:
                data.append({
                    "Id": row[0],
                    "Año": row[1],
                    datos + " Hombres": row[2],
                    datos + " Mujeres": row[3],
                    "Total " + datos: row[4]
            })
                # Imprimir la tabla en la consola
            tabla = tabulate.tabulate(data, headers="keys", tablefmt="pretty")
            print("\nRegistro encontrado:")
            print("-" * 90)
            print(tabla)
            print("-" * 90)
        else:
            print("-" * 90)
            print(f"No se encontró ningún registro.")
            print("-" * 90)
        
        while True:
            print("0- Volver")
            opcion = int(input("Ingrese una opcion: "))
            if opcion == 0:
                break
            else :
                print ("Por favor ingrese 0 para volver atras")
            
