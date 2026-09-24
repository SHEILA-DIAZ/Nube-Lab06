from dataclasses import dataclass
from datetime import time


@dataclass
class Entorno:
    hora: time
    pais: str
    dispositivo_corporativo: bool


@dataclass
class ResultadoABAC:
    permitido: bool
    motivos: list[str]


def politica_departamento(usuario, documento) -> tuple[bool, str]:
    if usuario.departamento_id != documento.departamento_id:
        return False, "El departamento del usuario no coincide con el documento."

    return True, "Departamento permitido."


def politica_nivel_seguridad(usuario, documento) -> tuple[bool, str]:
    if usuario.nivel_seguridad < documento.nivel_confidencialidad:
        return False, "El nivel de seguridad del usuario es insuficiente."

    return True, "Nivel de seguridad permitido."


def politica_propiedad(usuario, documento, accion: str) -> tuple[bool, str]:
    if accion == "MODIFICAR_DOCUMENTO":
        if usuario.rol.nombre == "EMPLEADO":
            if usuario.id != documento.propietario_id:
                return False, "El empleado solo puede modificar documentos propios."

    return True, "Propiedad permitida."


def politica_horario(documento, entorno: Entorno) -> tuple[bool, str]:
    if documento.nivel_confidencialidad >= 4:
        hora_inicio = time(8, 0)
        hora_fin = time(18, 0)

        if not (hora_inicio <= entorno.hora <= hora_fin):
            return False, "Los documentos confidenciales solo pueden accederse de 08:00 a 18:00."

    return True, "Horario permitido."


def politica_pais(documento, entorno: Entorno) -> tuple[bool, str]:
    if documento.pais.upper() == "PERU":
        if entorno.pais.upper() != "PERU":
            return False, "Los documentos de Perú solo pueden accederse desde Perú."

    return True, "País permitido."


def politica_dispositivo(documento, entorno: Entorno) -> tuple[bool, str]:
    if documento.nivel_confidencialidad >= 4:
        if not entorno.dispositivo_corporativo:
            return False, "Los documentos de alta confidencialidad requieren un dispositivo corporativo."

    return True, "Dispositivo permitido."


def politica_estado_usuario(usuario) -> tuple[bool, str]:
    if not usuario.estado:
        return False, "El usuario está inactivo."

    return True, "Usuario activo."


def politica_invitado(usuario, documento) -> tuple[bool, str]:
    if usuario.rol.nombre == "INVITADO":
        if usuario.tipo_contrato.upper() != "EXTERNO":
            return False, "El invitado debe tener contrato externo."

        if documento.nivel_confidencialidad > 1:
            return False, "Los invitados solo pueden acceder a documentos con confidencialidad máxima de nivel 1."

        if documento.estado.upper() != "PUBLICADO":
            return False, "Los invitados solo pueden acceder a documentos publicados."

    return True, "Restricciones de invitado permitidas."


def evaluar_abac(usuario, documento, accion: str, entorno: Entorno) -> ResultadoABAC:
    politicas = [
        politica_estado_usuario(usuario),
        politica_departamento(usuario, documento),
        politica_nivel_seguridad(usuario, documento),
        politica_propiedad(usuario, documento, accion),
        politica_horario(documento, entorno),
        politica_pais(documento, entorno),
        politica_dispositivo(documento, entorno),
        politica_invitado(usuario, documento),
    ]

    motivos = []

    for permitido, motivo in politicas:
        motivos.append(motivo)

        if not permitido:
            return ResultadoABAC(
                permitido=False,
                motivos=motivos
            )

    return ResultadoABAC(
        permitido=True,
        motivos=motivos
    )