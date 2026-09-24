from fastapi import FastAPI

from backend.app.api.routes.auth import router as auth_router

app = FastAPI(
    title="SecureDocs API",
    description="Sistema de gestión de expedientes con RBAC y ABAC",
    version="1.0.0"
)

app.include_router(auth_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "SecureDocs API funcionando",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }