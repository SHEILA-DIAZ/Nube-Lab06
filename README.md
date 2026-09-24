# SecureDocs

Sistema de gestión segura de documentos mediante autenticación, RBAC y ABAC.

## Descripción

SecureDocs permite gestionar documentos y controlar el acceso de los usuarios mediante:

- Autenticación con usuario y contraseña.
- Tokens JWT.
- RBAC (control basado en roles).
- ABAC (control basado en atributos).
- Gestión de documentos.
- Aprobación de documentos.
- Registro de auditoría.

## Tecnologías

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- Passlib / bcrypt
- Swagger / OpenAPI
- Git y GitHub

## Roles

- ADMINISTRADOR
- GERENTE
- SUPERVISOR
- EMPLEADO
- AUDITOR
- INVITADO

## Seguridad

El acceso se valida mediante RBAC y ABAC.

RBAC controla los permisos según el rol del usuario.

ABAC valida condiciones como:

- Departamento.
- Nivel de seguridad.
- Propiedad del documento.
- Horario.
- País.
- Dispositivo.
- Estado del usuario.
- Condiciones para invitados.

## Base de datos

El sistema utiliza SQLite con las tablas:

- departamentos
- roles
- permisos
- rol_permisos
- usuarios
- documentos
- auditoria

## Ejecución

Crear el entorno virtual:

py -m venv .venv

Activarlo:

.venv\Scripts\activate

Instalar dependencias:

pip install -r requirements.txt

Inicializar la base de datos:

python -m backend.app.database.init_db

Ejecutar:

uvicorn backend.app.main:app --reload

## Swagger

La documentación y pruebas de la API están disponibles en:

http://127.0.0.1:8000/docs

## Pruebas

Se realizaron pruebas de:

- Autorización RBAC.
- Políticas ABAC.
- Creación de documentos.
- Consulta de documentos.
- Modificación de documentos.
- Eliminación de documentos.
- Aprobación de documentos.
- Usuarios inactivos.
- Restricciones por departamento.
- Restricciones por nivel de seguridad.
- Restricciones por horario.
- Restricciones por país.
- Restricciones por dispositivo.
- Usuarios invitados.
- Auditoría.

## Repositorio

https://github.com/SHEILA-DIAZ/Nube-Lab06

## Autora

Sheila Diaz