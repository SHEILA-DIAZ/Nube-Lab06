from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.models import Usuario, Rol, Departamento
from backend.app.auth.dependencies import obtener_usuario_actual
from backend.app.auth.security import hash_password
from backend.app.services.rbac_service import tiene_permiso


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/")
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    if not tiene_permiso(
        usuario_actual.rol.nombre,
        "GESTIONAR_USUARIOS"
    ):
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para consultar usuarios"
        )

    usuarios = db.query(Usuario).all()

    return [
        {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol_id": usuario.rol_id,
            "departamento_id": usuario.departamento_id,
            "nivel_seguridad": usuario.nivel_seguridad,
            "pais": usuario.pais,
            "tipo_contrato": usuario.tipo_contrato,
            "estado": usuario.estado
        }
        for usuario in usuarios
    ]


@router.post("/")
def crear_usuario(
    datos: dict,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    if not tiene_permiso(
        usuario_actual.rol.nombre,
        "GESTIONAR_USUARIOS"
    ):
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para gestionar usuarios"
        )

    correo = datos.get("correo")

    if not correo:
        raise HTTPException(
            status_code=400,
            detail="El correo es obligatorio"
        )

    existente = db.query(Usuario).filter(
        Usuario.correo == correo
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    rol = db.query(Rol).filter(
        Rol.nombre == datos.get("rol", "EMPLEADO")
    ).first()

    if not rol:
        raise HTTPException(
            status_code=400,
            detail="Rol no encontrado"
        )

    departamento = db.query(Departamento).filter(
        Departamento.nombre == datos.get(
            "departamento",
            "TECNOLOGIA"
        )
    ).first()

    if not departamento:
        raise HTTPException(
            status_code=400,
            detail="Departamento no encontrado"
        )

    nuevo_usuario = Usuario(
        nombre=datos.get("nombre"),
        correo=correo,
        password_hash=hash_password(
            datos.get("password", "Usuario123")
        ),
        rol_id=rol.id,
        departamento_id=departamento.id,
        nivel_seguridad=datos.get("nivel_seguridad", 1),
        pais=datos.get("pais", "PERU"),
        tipo_contrato=datos.get(
            "tipo_contrato",
            "INTERNO"
        ),
        estado=datos.get("estado", True)
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario creado correctamente",
        "id": nuevo_usuario.id,
        "correo": nuevo_usuario.correo
    }


@router.put("/{usuario_id}")
def actualizar_usuario(
    usuario_id: int,
    datos: dict,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    if not tiene_permiso(
        usuario_actual.rol.nombre,
        "GESTIONAR_USUARIOS"
    ):
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para gestionar usuarios"
        )

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if "nombre" in datos:
        usuario.nombre = datos["nombre"]

    if "correo" in datos:
        usuario.correo = datos["correo"]

    if "password" in datos:
        usuario.password_hash = hash_password(
            datos["password"]
        )

    if "nivel_seguridad" in datos:
        usuario.nivel_seguridad = datos["nivel_seguridad"]

    if "pais" in datos:
        usuario.pais = datos["pais"]

    if "tipo_contrato" in datos:
        usuario.tipo_contrato = datos["tipo_contrato"]

    if "estado" in datos:
        usuario.estado = datos["estado"]

    if "rol" in datos:
        rol = db.query(Rol).filter(
            Rol.nombre == datos["rol"]
        ).first()

        if not rol:
            raise HTTPException(
                status_code=400,
                detail="Rol no encontrado"
            )

        usuario.rol_id = rol.id

    if "departamento" in datos:
        departamento = db.query(Departamento).filter(
            Departamento.nombre == datos["departamento"]
        ).first()

        if not departamento:
            raise HTTPException(
                status_code=400,
                detail="Departamento no encontrado"
            )

        usuario.departamento_id = departamento.id

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Usuario actualizado correctamente",
        "id": usuario.id,
        "correo": usuario.correo
    }