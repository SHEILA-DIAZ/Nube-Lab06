from fastapi import FastAPI

app = FastAPI(
    title="SecureDocs API",
    description="Sistema de gestión de expedientes con RBAC y ABAC",
    version="1.0.0"
)


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