from backend.app.services.rbac_service import tiene_permiso
from backend.app.policies.abac_policy import Entorno, evaluar_abac


def autorizar(
    usuario,
    documento,
    accion: str,
    entorno: Entorno
) -> tuple[bool, str]:

    # PASO 1: RBAC
    if not tiene_permiso(usuario.rol.nombre, accion):
        return False, f"RBAC deniega la acción: {accion}"

    # PASO 2: ABAC
    resultado_abac = evaluar_abac(
        usuario,
        documento,
        accion,
        entorno
    )

    if not resultado_abac.permitido:
        return False, f"ABAC deniega: {resultado_abac.motivos[-1]}"

    # PASO 3: Autorización concedida
    return True, "RBAC y ABAC permiten la operación."