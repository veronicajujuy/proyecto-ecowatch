from infraestructure.database import engine
from domain.models import Base
from services.log_loader import cargar_logs_csv
from services.log_repository import guardar_logs
from datetime import datetime

from cache.cache_temporal_logs import CacheTemporalLogs
from cache.depurador_logs import DepuradorLogs
import pandas as pd
from reports.reports_strategy import PromedioPorMetricaReport, AlertasCriticasReports
from reports.reports_factory import (
    PromedioPorMetricasVarias,
    AlertasCriticasVarias,
    ReporteFactory,
)


def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


def main():
    # ## crear tablas
    # create_tables()
    # print("Database setup complete.")

    # # cargar logs
    # ruta = "data/logs_ambientales_ecowatch.csv"
    # logs, errores = cargar_logs_csv(ruta)

    # print(f"Logs validos: {len(logs)}")
    # print(f"Logs validos: \n {logs}")
    # print(f"errores encontrados: {len(errores)}")

    # if errores:
    #     for fila, mensaje in errores:
    #         print(f"Error en linea {fila}, {mensaje}")

    # # guardar logs

    # guardar_logs(logs)

    ahora = datetime.fromisoformat("2025-05-01T08:05:00")

    depurador = DepuradorLogs(ventana_minutos=5)
    cache = CacheTemporalLogs.logs_desde_db(depurador=depurador, ahora=ahora)

    # mostramos los logs almacenados
    print("Logs almacenados en el cache:")
    i = 0
    for log in cache.obtener_todos():
        print(
            f"{log.timestamp} | {log.estado} | {log.temperatura} | {log.humedad} | {log.co2} | {log.mensaje}"
        )
        i += 1

    logs_dict = [log.dict() for log in cache.obtener_todos()]

    df = pd.DataFrame(logs_dict)
    print(df)

    # print(f"Logs almacenados: {i}")

    # cache.simular_tiempo(ahora=ahora, pasos=3)

    # reportes:

    # reporte de temperatura

    # reporte = PromedioPorMetricasVarias().generar_reporte(
    #     df, "temperatura", "humedad", "co2"
    # )
    # print(reporte)

    # reporte = AlertasCriticasVarias().generar_reporte(df, "WARNING", "ERROR")
    # print(reporte)

    reporte = ReporteFactory.elegir_reporte("promedio")
    print(reporte.generar_reporte(df, "temperatura", "humedad", "co2"))

    reporte = ReporteFactory.elegir_reporte("alertas")
    print(reporte.generar_reporte(df, "WARNING", "ERROR"))


if __name__ == "__main__":
    main()
