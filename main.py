from infraestructure.database import engine
from domain.models import Base
from services.log_loader import cargar_logs_csv
from services.log_repository import guardar_logs


def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


def main():
    ## crear tablas
    create_tables()
    print("Database setup complete.")

    # cargar logs
    ruta = "data/logs_ambientales_ecowatch.csv"
    logs, errores = cargar_logs_csv(ruta)

    print(f"Logs validos: {len(logs)}")
    print(f"Logs validos: \n {logs}")
    print(f"errores encontrados: {len(errores)}")

    if errores:
        for fila, mensaje in errores:
            print(f"Error en linea {fila}, {mensaje}")

    # guardar logs

    guardar_logs(logs)


if __name__ == "__main__":
    main()
