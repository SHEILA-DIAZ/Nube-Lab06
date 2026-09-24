from backend.app.database.database import SessionLocal
from backend.app.models.models import Usuario, Rol, Departamento
from backend.app.auth.security import hash_password


def crear_admin():
    db = SessionLocal()

    try:
        rol = db.query(Rol).filter(
            Rol.nombre == "ADMINISTRADOR"
        ).first()

        departamento = db.query(Departamento).filter(
            Departamento.nombre == "TECNOLOGIA"
        ).first()

        if not rol:
            print("ERROR: No existe el rol ADMINISTRADOR.")
            return

        if not departamento:
            print("ERROR: No existe el departamento TECNOLOGIA.")
            return

        usuario = db.query(Usuario).filter(
            Usuario.correo == "admin@securedocs.com"
        ).first()

        if not usuario:
            usuario = Usuario(
                nombre="Administrador SecureDocs",
                correo="admin@securedocs.com",
                password_hash=hash_password("Admin123"),
                rol_id=rol.id,
                departamento_id=departamento.id,
                nivel_seguridad=5,
                pais="PERU",
                tipo_contrato="INTERNO",
                estado=True
            )

            db.add(usuario)
            db.commit()

            print("Usuario administrador creado correctamente.")

        else:
            print("El usuario administrador ya existe.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    crear_admin()