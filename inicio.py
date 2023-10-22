while True:
    print(" ")
    print("-" * 30)
    print("Seccione que base de datos desea ver:")
    print("1. Emigracion")
    print("2. Inmigracion")
    print("3. Salir")
    print("-" * 30)

    opcion = input("Elige una opción (1/2/3): ")

    if opcion == "1":
        # Base de Emigracion
        try:
            import emigracion.py
            print("Base de datos de Emigracion ejecutado.")
        except ImportError:
            print(" ")
            
    elif opcion == "2":
        # Base de Inmigracion
        try:
            import inmigracion.py
            print("Base de datos de Inmigracion  ejecutado.")
        except ImportError:
            print(" ")
            
    elif opcion == "3":
        print("Saliendo...")
        break
    
    else:
        print("Opción no válida. Por favor, elige 1, 2 o 3.")

print("-" * 30)