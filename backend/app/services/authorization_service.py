from sqlalchemy.orm import Session

from backend.app.services.rbac_service import tiene_permiso
from backend.app.policies.abac_policy import Entorno, evaluar_abac
from backend.app.audit.audit_service import registrar_auditoria


def autorizar(
    usuario,
    documento,
    accion: str,
    entorno: Entorno,
    db: Session | None = None
) -> tuple[bool, str]:

    recurso = f"documento/{documento.id}"

    # Primero se verifica RBAC
    if not tiene_permiso(usuario.rol.nombre, accion):
        motivo = f"RBAC deniega la acción: {accion}"

        if db:
            registrar_auditoria(
                db=db,
                usuario=usuario.correo,
                recurso=recurso,
                accion=accion,
                resultado="DENEGADO",
                motivo=motivo
            )

        return False, motivo

    # Después se verifica ABAC
    resultado_abac = evaluar_abac(
        usuario,
        documento,
        accion,
        entorno
    )

    if not resultado_abac.permitido:
        motivo = f"ABAC deniega: {resultado_abac.motivos[-1]}"

        if db:
            registrar_auditoria(
                db=db,
                usuario=usuario.correo,
                recurso=recurso,
                accion=accion,
                resultado="DENEGADO",
                motivo=motivo
            )

        return False, motivo

    motivo = "RBAC y ABAC permiten la operación."

    if db:
        registrar_auditoria(
            db=db,
            usuario=usuario.correo,
            recurso=recurso,
            accion=accion,
            resultado="PERMITIDO",
            motivo=motivo
        )

    return True, motivo