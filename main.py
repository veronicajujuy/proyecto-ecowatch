from infraestructure.database import engine
from domain.models import Base
from services.log_loader import cargar_logs_csv
from services.log_repository import guardar_logs
from datetime import datetime
import os

from cache.cache_temporal_logs import CacheTemporalLogs
from cache.depurador_logs import DepuradorLogs
import pandas as pd
from reports.reports_factory import ReporteFactory
from reports.decorator import mostrar_encabezado_input


def cargar_datos_desde_csv():
    """(Usar solo si aún no hay datos en la base)"""

    Base.metadata.create_all(bind=engine)
    print("Creando tablas y cargando datos...")

    ruta = "data/logs_ambientales_ecowatch.csv"
    logs, errores = cargar_logs_csv(ruta)

    print(f"{len(logs)} logs cargados correctamente.")
    print(f"errores encontrados: {len(errores)}")

    guardar_logs(logs)
    input("\nPresione Enter para continuar...")


def mostrar_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print("\n--- EcoWatch - Reportes Ejecutivos ---")
    print("1. Generar reporte de promedios por métricas")
    print("2. Generar reporte de alertas críticas")
    print("3. Salir")


@mostrar_encabezado_input
def mostrar_promedio(df):
    reporte = ReporteFactory.elegir_reporte("promedio")
    return reporte.generar_reporte(df, "temperatura", "humedad", "co2")


@mostrar_encabezado_input
def mostrar_alertas(df):
    reporte = ReporteFactory.elegir_reporte("alertas")
    return reporte.generar_reporte(df, "WARNING", "ERROR")


def main():
    # cargar_datos_desde_csv()  # Descomentar solo si hace falta cargar datos

    ahora = datetime.fromisoformat("2025-05-01T08:05:00")
    depurador = DepuradorLogs(ventana_minutos=5)
    cache = CacheTemporalLogs.logs_desde_db(depurador=depurador, ahora=ahora)

    logs_dict = [log.dict() for log in cache.obtener_todos()]

    df = pd.DataFrame(logs_dict)
    print(df)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_promedio(df)

        elif opcion == "2":
            mostrar_alertas(df)

        elif opcion == "3":
            print("Saliendo...")
            break

        else:
            print("Opcion no reconocida")


if __name__ == "__main__":
    main()
