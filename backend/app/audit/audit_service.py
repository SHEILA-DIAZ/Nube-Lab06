from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.models.models import Auditoria


def registrar_auditoria(
    db: Session,
    usuario: str,
    recurso: str,
    accion: str,
    resultado: str,
    motivo: str
):
    registro = Auditoria(
        usuario=usuario,
        recurso=recurso,
        accion=accion,
        fecha=datetime.utcnow(),
        resultado=resultado,
        motivo=motivo
    )

    db.add(registro)
    db.commit()
    db.refresh(registro)

    return registro