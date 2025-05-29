def mostrar_encabezado_input(func):
    def wrapper(*args, **kwargs):
        print("\n--- REPORTE GENERADO ---\n")
        resultado = func(*args, **kwargs)
        print(resultado)
        input("\nPresione Enter para volver al menú...")
        return resultado

    return wrapper
