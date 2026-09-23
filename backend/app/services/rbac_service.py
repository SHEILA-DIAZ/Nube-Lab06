from sqlalchemy.orm import Session

from backend.app.models.models import Rol


PERMISOS_POR_ROL = {
    "ADMINISTRADOR": {
        "CREAR_DOCUMENTO",
        "CONSULTAR_DOCUMENTO",
        "MODIFICAR_DOCUMENTO",
        "ELIMINAR_DOCUMENTO",
        "APROBAR_DOCUMENTO",
        "VER_AUDITORIA",
        "GESTIONAR_USUARIOS",
        "ASIGNAR_ROLES",
    },
    "GERENTE": {
        "CREAR_DOCUMENTO",
        "CONSULTAR_DOCUMENTO",
        "MODIFICAR_DOCUMENTO",
        "ELIMINAR_DOCUMENTO",
        "APROBAR_DOCUMENTO",
        "VER_AUDITORIA",
    },
    "SUPERVISOR": {
        "CREAR_DOCUMENTO",
        "CONSULTAR_DOCUMENTO",
        "MODIFICAR_DOCUMENTO",
        "APROBAR_DOCUMENTO",
    },
    "EMPLEADO": {
        "CREAR_DOCUMENTO",
        "CONSULTAR_DOCUMENTO",
        "MODIFICAR_DOCUMENTO",
    },
    "AUDITOR": {
        "CONSULTAR_DOCUMENTO",
        "VER_AUDITORIA",
    },
    "INVITADO": {
        "CONSULTAR_DOCUMENTO",
    },
}


def tiene_permiso(rol_nombre: str, permiso: str) -> bool:
    permisos = PERMISOS_POR_ROL.get(rol_nombre, set())
    return permiso in permisos


def obtener_permisos(rol_nombre: str) -> set[str]:
    return PERMISOS_POR_ROL.get(rol_nombre, set())