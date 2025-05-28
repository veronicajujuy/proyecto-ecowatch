import csv
from datetime import datetime
from domain.models import LogRaw
from config import EXPECTED_FIELDS


def cargar_logs_csv(ruta):
    logs_validos = []
    errores = []

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for i, fila in enumerate(lector, start=1):
            try:
                # validar campos clave
                if not all(campo in fila for campo in EXPECTED_FIELDS):
                    raise ValueError(f"Campos faltantes en la fila {i}")

                # parsear y validar tipos
                timestamp = datetime.fromisoformat(fila["timestamp"])
                sala_nombre = fila["sala"]
                estado = fila["estado"]
                temperatura = float(fila["temperatura"])
                humedad = float(fila["humedad"])
                co2 = int(fila["co2"])
                mensaje = fila["mensaje"]

                # crear instancia de log (no agregar sala)
                log = LogRaw(
                    timestamp=timestamp,
                    estado=estado,
                    temperatura=temperatura,
                    humedad=humedad,
                    co2=co2,
                    mensaje=mensaje,
                )
                logs_validos.append((sala_nombre, log))

            except Exception as e:
                errores.append((i, str(e)))

    return logs_validos, errores
