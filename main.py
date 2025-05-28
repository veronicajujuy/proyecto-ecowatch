from infraestructure.database import engine
from domain.models import Base
from services.log_loader import cargar_logs_csv
from services.log_repository import guardar_logs
from datetime import datetime

from cache.cache_temporal_logs import CacheTemporalLogs
from cache.depurador_logs import DepuradorLogs


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

    print(f"Logs almacenados: {i}")

    cache.simular_tiempo(ahora=ahora, pasos=3)


if __name__ == "__main__":
    main()
