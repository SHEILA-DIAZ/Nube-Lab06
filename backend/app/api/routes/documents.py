from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.models import Documento
from backend.app.schemas.document import (
    DocumentoActualizar,
    DocumentoCrear,
    DocumentoRespuesta
)
from backend.app.policies.abac_policy import Entorno
from backend.app.services.authorization_service import autorizar
from backend.app.auth.dependencies import obtener_usuario_actual


router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"]
)


def crear_entorno():
    return Entorno(
        hora=datetime.now().time(),
        pais="PERU",
        dispositivo_corporativo=True
    )


@router.post("/", response_model=DocumentoRespuesta)
def crear_documento(
    datos: DocumentoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    documento_temp = Documento(
        id=0,
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        propietario_id=usuario.id,
        departamento_id=datos.departamento_id,
        nivel_confidencialidad=datos.nivel_confidencialidad,
        estado="PENDIENTE",
        pais=datos.pais,
        fecha_creacion=datetime.utcnow()
    )

    permitido, motivo = autorizar(
        usuario,
        documento_temp,
        "CREAR_DOCUMENTO",
        crear_entorno(),
        db=db
    )

    if not permitido:
        raise HTTPException(
            status_code=403,
            detail=motivo
        )

    documento = Documento(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        propietario_id=usuario.id,
        departamento_id=datos.departamento_id,
        nivel_confidencialidad=datos.nivel_confidencialidad,
        estado="PENDIENTE",
        pais=datos.pais,
        fecha_creacion=datetime.utcnow()
    )

    db.add(documento)
    db.commit()
    db.refresh(documento)

    return documento


@router.get("/", response_model=list[DocumentoRespuesta])
def listar_documentos(
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    documentos = db.query(Documento).all()

    documentos_permitidos = []

    for documento in documentos:
        permitido, _ = autorizar(
            usuario,
            documento,
            "CONSULTAR_DOCUMENTO",
            crear_entorno(),
            db=db
        )

        if permitido:
            documentos_permitidos.append(documento)

    return documentos_permitidos


@router.get("/{documento_id}", response_model=DocumentoRespuesta)
def obtener_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    documento = (
        db.query(Documento)
        .filter(Documento.id == documento_id)
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    permitido, motivo = autorizar(
        usuario,
        documento,
        "CONSULTAR_DOCUMENTO",
        crear_entorno(),
        db=db
    )

    if not permitido:
        raise HTTPException(
            status_code=403,
            detail=motivo
        )

    return documento


@router.put("/{documento_id}", response_model=DocumentoRespuesta)
def modificar_documento(
    documento_id: int,
    datos: DocumentoActualizar,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    documento = (
        db.query(Documento)
        .filter(Documento.id == documento_id)
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    permitido, motivo = autorizar(
        usuario,
        documento,
        "MODIFICAR_DOCUMENTO",
        crear_entorno(),
        db=db
    )

    if not permitido:
        raise HTTPException(
            status_code=403,
            detail=motivo
        )

    if datos.titulo is not None:
        documento.titulo = datos.titulo

    if datos.descripcion is not None:
        documento.descripcion = datos.descripcion

    if datos.departamento_id is not None:
        documento.departamento_id = datos.departamento_id

    if datos.nivel_confidencialidad is not None:
        documento.nivel_confidencialidad = datos.nivel_confidencialidad

    if datos.pais is not None:
        documento.pais = datos.pais

    db.commit()
    db.refresh(documento)

    return documento


@router.delete("/{documento_id}")
def eliminar_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    documento = (
        db.query(Documento)
        .filter(Documento.id == documento_id)
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    permitido, motivo = autorizar(
        usuario,
        documento,
        "ELIMINAR_DOCUMENTO",
        crear_entorno(),
        db=db
    )

    if not permitido:
        raise HTTPException(
            status_code=403,
            detail=motivo
        )

    db.delete(documento)
    db.commit()

    return {
        "mensaje": "Documento eliminado correctamente",
        "documento_id": documento_id
    }


@router.post(
    "/{documento_id}/aprobar",
    response_model=DocumentoRespuesta
)
def aprobar_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual)
):
    documento = (
        db.query(Documento)
        .filter(Documento.id == documento_id)
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    permitido, motivo = autorizar(
        usuario,
        documento,
        "APROBAR_DOCUMENTO",
        crear_entorno(),
        db=db
    )

    if not permitido:
        raise HTTPException(
            status_code=403,
            detail=motivo
        )

    documento.estado = "APROBADO"

    db.commit()
    db.refresh(documento)

    return documento