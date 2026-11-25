import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from app.models.palavra import Palavra


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    session.add_all([
        Palavra(palavra="TERMO"),
        Palavra(palavra="PENSO"),
        Palavra(palavra="ARARA"),
    ])
    session.commit()

    yield session
    session.close()
    engine.dispose()

@pytest.fixture
def client(db):
    def get_db_de_teste():
        yield db

    app.dependency_overrides[get_db] = get_db_de_teste
    yield TestClient(app)
    app.dependency_overrides.clear()
