from backend.app.database.database import SessionLocal
from backend.app.models.models import Usuario, Rol, Departamento
from backend.app.auth.security import hash_password


USUARIOS = [
    {
        "nombre": "Gerente Principal",
        "correo": "gerente@securedocs.com",
        "password": "Gerente123",
        "rol": "GERENTE",
        "departamento": "TECNOLOGIA",
        "nivel_seguridad": 5,
        "pais": "PERU",
        "tipo_contrato": "INTERNO",
        "estado": True,
    },
    {
        "nombre": "Supervisor Principal",
        "correo": "supervisor@securedocs.com",
        "password": "Supervisor123",
        "rol": "SUPERVISOR",
        "departamento": "TECNOLOGIA",
        "nivel_seguridad": 3,
        "pais": "PERU",
        "tipo_contrato": "INTERNO",
        "estado": True,
    },
    {
        "nombre": "Empleado Principal",
        "correo": "empleado@securedocs.com",
        "password": "Empleado123",
        "rol": "EMPLEADO",
        "departamento": "TECNOLOGIA",
        "nivel_seguridad": 2,
        "pais": "PERU",
        "tipo_contrato": "INTERNO",
        "estado": True,
    },
    {
        "nombre": "Auditor Principal",
        "correo": "auditor@securedocs.com",
        "password": "Auditor123",
        "rol": "AUDITOR",
        "departamento": "TECNOLOGIA",
        "nivel_seguridad": 5,
        "pais": "PERU",
        "tipo_contrato": "INTERNO",
        "estado": True,
    },
    {
        "nombre": "Invitado Externo",
        "correo": "invitado@securedocs.com",
        "password": "Invitado123",
        "rol": "INVITADO",
        "departamento": "TECNOLOGIA",
        "nivel_seguridad": 1,
        "pais": "PERU",
        "tipo_contrato": "EXTERNO",
        "estado": True,
    },
    {
        "nombre": "Empleado Inactivo",
        "correo": "empleado.inactivo@securedocs.com",
        "password": "Inactivo123",
        "rol": "EMPLEADO",
        "departamento": "TECNOLOGIA",
        "nivel_seguridad": 2,
        "pais": "PERU",
        "tipo_contrato": "INTERNO",
        "estado": False,
    },
]


def obtener_rol(db, nombre):
    return (
        db.query(Rol)
        .filter(Rol.nombre == nombre)
        .first()
    )


def obtener_departamento(db, nombre):
    return (
        db.query(Departamento)
        .filter(Departamento.nombre == nombre)
        .first()
    )


def crear_usuarios():
    db = SessionLocal()

    try:
        for datos in USUARIOS:
            usuario_existente = (
                db.query(Usuario)
                .filter(Usuario.correo == datos["correo"])
                .first()
            )

            if usuario_existente:
                print(f"Ya existe: {datos['correo']}")
                continue

            rol = obtener_rol(db, datos["rol"])
            departamento = obtener_departamento(
                db,
                datos["departamento"]
            )

            if not rol:
                print(f"No existe el rol: {datos['rol']}")
                continue

            if not departamento:
                print(
                    f"No existe el departamento: "
                    f"{datos['departamento']}"
                )
                continue

            usuario = Usuario(
                nombre=datos["nombre"],
                correo=datos["correo"],
                password_hash=hash_password(datos["password"]),
                rol_id=rol.id,
                departamento_id=departamento.id,
                nivel_seguridad=datos["nivel_seguridad"],
                pais=datos["pais"],
                tipo_contrato=datos["tipo_contrato"],
                estado=datos["estado"],
            )

            db.add(usuario)
            db.commit()
            db.refresh(usuario)

            print(
                f"Usuario creado: "
                f"{usuario.correo} | "
                f"Rol: {rol.nombre}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    crear_usuarios()
    print("Proceso de usuarios finalizado.")