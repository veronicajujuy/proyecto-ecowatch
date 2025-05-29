from datetime import datetime

from pydantic import BaseModel


# @dataclass
class LogEntry(BaseModel):
    timestamp: datetime
    sala: str
    estado: str  # Ej: INFO, ERROR, WARN
    temperatura: float
    humedad: float
    co2: int
    mensaje: str

    def __lt__(self, other: "LogEntry"):
        """Compara dos objetos LogEntry basándose en sus timestamps."""
        assert isinstance(other, LogEntry), NotImplemented
        return self.timestamp < other.timestamp

    @staticmethod
    def from_db_row(row: tuple) -> "LogEntry":
        """Crea una instancia de LogEntry desde una tupla de la base de datos."""
        return LogEntry(
            timestamp=datetime.fromisoformat(row[0]),
            sala=row[1],
            estado=row[2],
            temperatura=row[3],
            humedad=row[4],
            co2=row[5],
            mensaje=row[6],
        )

    class Config:
        frozen = True
