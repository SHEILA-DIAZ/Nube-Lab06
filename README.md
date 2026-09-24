\# SecureDocs



Sistema web para la gestión segura de documentos mediante autenticación, autorización RBAC y políticas ABAC.



\## Descripción



SecureDocs es una aplicación web desarrollada para gestionar documentos y controlar el acceso a los recursos mediante un modelo combinado de:



\- Autenticación mediante usuario y contraseña.

\- Tokens JWT.

\- Control de acceso basado en roles (RBAC).

\- Control de acceso basado en atributos (ABAC).

\- Registro de auditoría.

\- Gestión de documentos.

\- Aprobación de documentos.



La autorización se realiza mediante la evaluación conjunta de RBAC y ABAC.



\## Tecnologías utilizadas



\- Python

\- FastAPI

\- SQLAlchemy

\- SQLite

\- Pydantic

\- JWT

\- Passlib / bcrypt

\- HTML, CSS y JavaScript

\- Swagger / OpenAPI

\- Git y GitHub



\## Estructura del proyecto



```text

Nube-Lab06/

│

├── backend/

│   └── app/

│       ├── api/

│       ├── auth/

│       ├── audit/

│       ├── core/

│       ├── database/

│       ├── models/

│       ├── policies/

│       ├── routes/

│       ├── schemas/

│       └── services/

│

├── frontend/

├── docs/

├── tests/

├── .gitignore

├── README.md

└── requirements.txt

