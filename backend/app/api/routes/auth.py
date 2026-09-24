from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.models import Usuario
from backend.app.schemas.auth import LoginRequest, TokenResponse
from backend.app.auth.security import verify_password
from backend.app.auth.jwt import crear_token


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    datos: LoginRequest,
    db: Session = Depends(get_db)
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.correo == datos.correo)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    # El campo estado es booleano:
    # True = activo
    # False = inactivo
    if not usuario.estado:
        raise HTTPException(
            status_code=403,
            detail="Usuario inactivo"
        )

    if not verify_password(
        datos.password,
        usuario.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    token = crear_token({
        "sub": str(usuario.id),
        "correo": usuario.correo,
        "rol": usuario.rol.nombre
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }