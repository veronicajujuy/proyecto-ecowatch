from collections import deque
from datetime import datetime, timedelta

from sortedcontainers import SortedDict

from domain.log_entry import LogEntry


class DepuradorLogs:
    def __init__(self, ventana_minutos: int):
        self.__ventana_minutos = ventana_minutos
        self.__timestamps: deque[datetime] = deque()

    @property
    def ventana_minutos(self) -> int:
        return self.__ventana_minutos

    def registrar_timestamp(self, timestamp: datetime) -> "DepuradorLogs":
        """Registra un nuevo timestamp para el seguimiento temporal de logs
        Este método matiene un registro ordenado de timestamps que se utilizan
        para determinar si un log es antiguo o reciente
         Args:
            timestamp (datetime): Marca temporal del log a registrar

        Returns:
            DepuradorLogs: Retorna self para permitir encadenamiento de métodos
        """
        self.__timestamps.append(timestamp)
        return self

    def depurar_logs(self, cache_logs: SortedDict, ahora: datetime) -> list[LogEntry]:
        """Elimina logs antiguos basándose en una ventana temporal deslizante.

        1. Encuentra el timestamp más reciente
        2. Calcula un umbral restando ventana_minutos al más reciente
        3. Elimina todos los logs anteriores al umbral

        Args:
            cache_logs (SortedDict): Diccionario ordenado que contiene los logs,
                                     donde las claves son timestamps y los valores
                                     son listas de LogEntry

        Returns:
            list[LogEntry]: Lista de logs que fueron eliminados del cache
        """
        # if not self.__timestamps:
        #     return []

        # mas_reciente: datetime = max(self.__timestamps)
        umbral: datetime = ahora - timedelta(minutes=self.__ventana_minutos)
        eliminados = []

        claves_a_eliminar = [
            timestamp for timestamp in cache_logs if timestamp < umbral
        ]

        for clave in claves_a_eliminar:
            eliminados.extend(cache_logs.pop(clave))

        return eliminados

    def obtener_umbral_actual(self) -> datetime | None:
        """Devuelve el umbral actual calculado con base en el timestamp más reciente.

        Returns:
            datetime | None: Timestamp umbral, o None si no hay timestamps registrados
        """
        if not self.__timestamps:
            return None
        return max(self.__timestamps) - timedelta(minutes=self.__ventana_minutos)

    def limpiar_todo(self) -> None:
        """Limpia completamente los timestamps registrados."""
        self.__timestamps.clear()
