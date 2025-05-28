from datetime import datetime, timedelta
from sortedcontainers import SortedDict
from domain.log_entry import LogEntry
from cache.depurador_logs import DepuradorLogs
from domain.models import LogRaw, Sala
from infraestructure.database import SessionLocal


class CacheTemporalLogs:
    def __init__(self, depurador: DepuradorLogs):
        self.__depurador: DepuradorLogs = depurador
        self.__cache: SortedDict = SortedDict()

    def agregar_log(self, log: LogEntry) -> "CacheTemporalLogs":
        """Agrega un nuevo log al cache en memoria.

        1. Registra el timestamp en el depurador
        2. Agrega el log en el diccionario agrupado por timestamp

        Args:
            log (LogEntry): Log a almacenar en memoria

        Returns:
            CacheTemporalLogs: self para permitir encadenamiento
        """
        timestamp: datetime = log.timestamp
        self.__depurador.registrar_timestamp(timestamp)

        # print(f"Registramos timestamp: {timestamp}")
        # print(f"Depurador: {self.__cache}")

        if timestamp not in self.__cache:
            self.__cache[timestamp] = []
        self.__cache[timestamp].append(log)
        return self

    def obtener_logs(self, desde: datetime, hasta: datetime) -> list[LogEntry]:
        """Obtiene todos los logs en el rango de fechas especificado.

        Args:
            desde (datetime): Fecha inicial del rango
            hasta (datetime): Fecha final del rango

        Returns:
            list[LogEntry]: Lista de logs en el rango especificado
        """
        logs: list[LogEntry] = []

        for timestamp in self.__cache.irange(desde, hasta, inclusive=(True, True)):
            logs.extend(self.__cache[timestamp])
        return logs

    def obtener_todos(self) -> list[LogEntry]:
        """Obtiene todos los logs almacenados en el cache.

        Returns:
            list[LogEntry]: Lista de todos los logs almacenados en el cache ordenados temporalmente
        """
        logs: list[LogEntry] = []
        for lista in self.__cache.values():
            logs.extend(lista)
        return logs

    def depurar(self, ahora: datetime) -> list[LogEntry]:
        """Elimina logs antiguos basándose en la ventana temporal del depurador.

        Returns:
            list[LogEntry]: Lista de logs eliminados del cache
        """
        return self.__depurador.depurar_logs(self.__cache, ahora)

    def actualizar_desde_db(self, ahora: datetime):
        session = SessionLocal()

        try:
            umbral = ahora - timedelta(minutes=self.__depurador.ventana_minutos)
            print(f"Umbral: {umbral} , ahora: {ahora}")
            logs_bd = (
                session.query(LogRaw)
                .join(Sala, Sala.id == LogRaw.sala_id)
                .filter(LogRaw.timestamp >= umbral, LogRaw.timestamp <= ahora)
                .all()
            )

            for log in logs_bd:
                entrada = LogEntry(
                    timestamp=log.timestamp,
                    estado=log.estado,
                    temperatura=log.temperatura,
                    humedad=log.humedad,
                    co2=log.co2,
                    mensaje=log.mensaje,
                    sala=log.sala.nombre,
                )
                self.agregar_log(entrada)

        except Exception as e:
            print(f"Error al obtener logs desde la base de datos: {e}")

        finally:
            session.close()

    @classmethod
    def logs_desde_db(
        cls, depurador: DepuradorLogs, ahora: datetime
    ) -> "CacheTemporalLogs":
        """Carga los logs desde la base de datos de los ultimos x minutos desde
        un 'ahora' dado.
        Args:
            depurador (DepuradorLogs): Depurador de logs
            ahora (datetime): Hora que se seteara como el 'ahora'
        Returns:
            CacheTemporalLogs: CacheTemporalLogs
        """
        cache = cls(depurador=depurador)
        cache.actualizar_desde_db(ahora)

        return cache

    def simular_tiempo(self, ahora: datetime, pasos: int = 5):
        """Simula la evolución del tiempo y depura logs cada minuto.

        Args:
            ahora (datetime): Hora de inicio de la simulación
            pasos (int): Número de pasos (minutos) a simular
        """
        actual = ahora
        for i in range(pasos):
            print(f"\n\n--- Tiempo simulado: {actual} ---")
            eliminados = self.depurar(actual)
            print(
                f"Logs eliminados: {[log.timestamp.strftime('%H:%M:%S') for log in eliminados]}"
            )
            self.actualizar_desde_db(actual)
            print(
                f"Logs restantes: {[log.timestamp.strftime('%H:%M:%S') for log in self.obtener_todos()]}"
            )
            actual += timedelta(minutes=1)
