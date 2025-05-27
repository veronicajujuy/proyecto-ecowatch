from sqlalchemy.orm import Session
from domain.models import Sala, Log
from infraestructure.database import SessionLocal


def guardar_logs(lista_logs):
    session: Session = SessionLocal()

    try:
        for sala_nombre, log in lista_logs:
            sala = session.query(Sala).filter_by(nombre=sala_nombre).first()

            if sala is None:
                sala = Sala(nombre=sala_nombre)
                session.add(sala)
                session.flush()

            log.sala = sala

            session.add(log)

        session.commit()
        print(f"Se guardaron {len(lista_logs)} logs en la base de datos")

    except Exception as e:
        session.rollback()
        print(f"Ocurrio un error al guardar los logs: {str(e)}")

    finally:
        session.close()
