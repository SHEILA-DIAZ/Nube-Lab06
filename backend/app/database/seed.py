from backend.app.database.database import SessionLocal
from backend.app.models.models import Departamento, Permiso, Rol, RolPermiso


ROLES = [
    "ADMINISTRADOR",
    "GERENTE",
    "SUPERVISOR",
    "EMPLEADO",
    "AUDITOR",
    "INVITADO",
]

PERMISOS = [
    "CREAR_DOCUMENTO",
    "CONSULTAR_DOCUMENTO",
    "MODIFICAR_DOCUMENTO",
    "ELIMINAR_DOCUMENTO",
    "APROBAR_DOCUMENTO",
    "VER_AUDITORIA",
    "GESTIONAR_USUARIOS",
    "ASIGNAR_ROLES",
]

PERMISOS_POR_ROL = {
    "ADMINISTRADOR": PERMISOS,
    "GERENTE": [
        "CREAR_DOCUMENTO",
        "CONSULTAR_DOCUMENTO",
        "MODIFICAR_DOCUMENTO",
        "ELIMINAR_DOCUMENTO",
        "APROBAR_DOCUMENTO",
        "VER_AUDITORIA",
    ],
    "SUPERVISOR": [
        "CREAR_DOCUMENTO",
        "CONSULTAR_DOCUMENTO",
        "MODIFICAR_DOCUMENTO",
        "APROBAR_DOCUMENTO",
    ],
    "EMPLEADO": [
        "CREAR_DOCUMENTO",
        "CONSULTAR_DOCUMENTO",
        "MODIFICAR_DOCUMENTO",
    ],
    "AUDITOR": [
        "CONSULTAR_DOCUMENTO",
        "VER_AUDITORIA",
    ],
    "INVITADO": [
        "CONSULTAR_DOCUMENTO",
    ],
}

DEPARTAMENTOS = [
    "FINANZAS",
    "RRHH",
    "TECNOLOGIA",
    "OPERACIONES",
]


def seed():
    db = SessionLocal()

    try:
        roles = {}

        for nombre in ROLES:
            rol = db.query(Rol).filter(Rol.nombre == nombre).first()

            if not rol:
                rol = Rol(nombre=nombre)
                db.add(rol)
                db.flush()

            roles[nombre] = rol

        permisos = {}

        for nombre in PERMISOS:
            permiso = (
                db.query(Permiso)
                .filter(Permiso.nombre == nombre)
                .first()
            )

            if not permiso:
                permiso = Permiso(nombre=nombre)
                db.add(permiso)
                db.flush()

            permisos[nombre] = permiso

        for nombre_rol, nombres_permisos in PERMISOS_POR_ROL.items():
            rol = roles[nombre_rol]

            for nombre_permiso in nombres_permisos:
                permiso = permisos[nombre_permiso]

                existente = (
                    db.query(RolPermiso)
                    .filter(
                        RolPermiso.rol_id == rol.id,
                        RolPermiso.permiso_id == permiso.id,
                    )
                    .first()
                )

                if not existente:
                    db.add(
                        RolPermiso(
                            rol_id=rol.id,
                            permiso_id=permiso.id,
                        )
                    )

        for nombre in DEPARTAMENTOS:
            existe = (
                db.query(Departamento)
                .filter(Departamento.nombre == nombre)
                .first()
            )

            if not existe:
                db.add(Departamento(nombre=nombre))

        db.commit()

        print("Datos RBAC iniciales creados correctamente.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()