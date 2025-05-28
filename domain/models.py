from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from infraestructure.database import Base
from datetime import datetime
from abc import abstractmethod, ABC


class Sala(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)

    # Relación con logs 1:a N:
    logs = relationship("Log", back_populates="sala")

    def __repr__(self):
        return f"<Sala(id={self.id}, nombre='{self.nombre}')>"


class Log(Base):
    __tablename__ = "logs"
    __table_args__ = (
        UniqueConstraint("timestamp", "sala_id", name="unique_log_por_sala_y_tiempo"),
    )
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    estado = Column(String(20), nullable=False)
    temperatura = Column(Float)
    humedad = Column(Float)
    co2 = Column(Integer)
    mensaje = Column(String(255))

    # Relación N :a 1 con Sala
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False)
    sala = relationship("Sala", back_populates="logs")

    def __repr__(self):
        return f"<Log(id={self.id}, timestamp={self.timestamp}, estado='{self.estado}', temperatura={self.temperatura}, humedad={self.humedad}, co2={self.co2})>"


class Reporte(ABC):
    @abstractmethod
    def generar(self, datos):
        pass
