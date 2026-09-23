from backend.app.database.database import Base, engine
from backend.app.models import models


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Base de datos creada correctamente.")