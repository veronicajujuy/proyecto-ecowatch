from sqlalchemy.orm import Session
from domain.models import Sala, Log
from infraestructure.database import SessionLocal
from sqlalchemy.exc import IntegrityError


def guardar_logs(lista_logs):
    session: Session = SessionLocal()

    guardados = 0
    duplicados = 0

    try:
        for sala_nombre, log in lista_logs:
            sala = session.query(Sala).filter_by(nombre=sala_nombre).first()

            if sala is None:
                sala = Sala(nombre=sala_nombre)
                session.add(sala)
                session.flush()

            log.sala = sala

            try:
                with session.begin_nested():
                    session.add(log)
                    session.flush()

                    guardados += 1

            except IntegrityError:
                print(f"[SKIP] Duplicado: {sala.nombre} - {log.timestamp}")
                duplicados += 1
                continue

        session.commit()
        print(f"Se guardaron {guardados} logs en la base de datos")
        print(f"duplicados {duplicados} logs en la base de datos")

    except Exception as e:
        session.rollback()
        print(f"Ocurrio un error al guardar los logs: {str(e)}")

    finally:
        session.close()
