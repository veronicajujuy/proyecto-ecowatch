from sqlalchemy.orm import Session
from domain.models import Sala, LogRaw
from infraestructure.database import SessionLocal
from sqlalchemy.exc import IntegrityError


def guardar_logs(lista_logs):
    session: Session = SessionLocal()

    guardados = 0

    try:
        for sala_nombre, log in lista_logs:
            sala = session.query(Sala).filter_by(nombre=sala_nombre).first()

            if sala is None:
                sala = Sala(nombre=sala_nombre)
                session.add(sala)
                session.flush()

            log_raw = LogRaw(
                timestamp=log.timestamp,
                estado=log.estado,
                temperatura=log.temperatura,
                humedad=log.humedad,
                co2=log.co2,
                mensaje=log.mensaje,
                sala=sala,
            )

            session.add(log_raw)

            guardados += 1

        session.commit()
        print(f"Se guardaron {guardados} logs en la base de datos")

    except Exception as e:
        session.rollback()
        print(f"Ocurrio un error al guardar los logs: {str(e)}")

    finally:
        session.close()
