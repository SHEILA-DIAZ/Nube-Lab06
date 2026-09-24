from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.models import Auditoria, Usuario
from backend.app.auth.dependencies import obtener_usuario_actual
from backend.app.services.rbac_service import tiene_permiso


router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoría"]
)


@router.get("/")
def listar_auditoria(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    if not tiene_permiso(
        usuario_actual.rol.nombre,
        "VER_AUDITORIA"
    ):
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para consultar la auditoría"
        )

    registros = (
        db.query(Auditoria)
        .order_by(Auditoria.fecha.desc())
        .all()
    )

    return [
        {
            "id": registro.id,
            "usuario": registro.usuario,
            "recurso": registro.recurso,
            "accion": registro.accion,
            "fecha": registro.fecha,
            "resultado": registro.resultado,
            "motivo": registro.motivo
        }
        for registro in registros
    ]