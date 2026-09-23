from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.database import Base


class Departamento(Base):
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="departamento")
    documentos = relationship("Documento", back_populates="departamento")


class Rol(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship("RolPermiso", back_populates="rol")


class Permiso(Base):
    __tablename__ = "permisos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    roles = relationship("RolPermiso", back_populates="permiso")


class RolPermiso(Base):
    __tablename__ = "rol_permisos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    permiso_id: Mapped[int] = mapped_column(ForeignKey("permisos.id"), nullable=False)

    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    departamento_id: Mapped[int] = mapped_column(
        ForeignKey("departamentos.id"),
        nullable=False
    )

    nivel_seguridad: Mapped[int] = mapped_column(Integer, default=1)
    pais: Mapped[str] = mapped_column(String(50), default="PERU")
    tipo_contrato: Mapped[str] = mapped_column(String(30), default="INTERNO")
    estado: Mapped[bool] = mapped_column(Boolean, default=True)

    rol = relationship("Rol", back_populates="usuarios")
    departamento = relationship("Departamento", back_populates="usuarios")
    documentos = relationship("Documento", back_populates="propietario")


class Documento(Base):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=True)

    propietario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    departamento_id: Mapped[int] = mapped_column(
        ForeignKey("departamentos.id"),
        nullable=False
    )

    nivel_confidencialidad: Mapped[int] = mapped_column(Integer, default=1)
    estado: Mapped[str] = mapped_column(String(30), default="PENDIENTE")
    pais: Mapped[str] = mapped_column(String(50), default="PERU")
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    propietario = relationship("Usuario", back_populates="documentos")
    departamento = relationship("Departamento", back_populates="documentos")


class Auditoria(Base):
    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario: Mapped[str] = mapped_column(String(150), nullable=False)
    recurso: Mapped[str] = mapped_column(String(150), nullable=False)
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    resultado: Mapped[str] = mapped_column(String(30), nullable=False)
    motivo: Mapped[str] = mapped_column(String(255), nullable=True)