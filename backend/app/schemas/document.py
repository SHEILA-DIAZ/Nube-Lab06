
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentoBase(BaseModel):
    titulo: str
    descripcion: str | None = None
    departamento_id: int
    nivel_confidencialidad: int
    pais: str = "PERU"


class DocumentoCrear(DocumentoBase):
    pass


class DocumentoActualizar(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    departamento_id: int | None = None
    nivel_confidencialidad: int | None = None
    pais: str | None = None


class DocumentoRespuesta(DocumentoBase):
    id: int
    propietario_id: int
    estado: str
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)