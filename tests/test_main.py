import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_crud_lifecycle():
    # Create
    resp = client.post(
        "/employees/",
        json={
            "full_name": "Sanchit",
            "job_title": "Dev",
            "country": "India",
            "salary": 1000,
        },
    )
    emp_id = resp.json()["id"]
    assert resp.status_code == 201

    # Update
    update_resp = client.put(
        f"/employees/{emp_id}",
        json={
            "full_name": "Sanchit S",
            "job_title": "Sr Dev",
            "country": "India",
            "salary": 2000,
        },
    )
    assert update_resp.json()["salary"] == 2000

    # Delete
    del_resp = client.delete(f"/employees/{emp_id}")
    assert del_resp.status_code == 204


def test_salary_logic():
    client.post(
        "/employees/",
        json={
            "full_name": "A",
            "job_title": "Dev",
            "country": "India",
            "salary": 10000,
        },
    )
    response = client.get("/employees/1/salary")
    assert response.json()["net_salary"] == 9000.0


def test_metrics():
    client.post(
        "/employees/",
        json={
            "full_name": "A",
            "job_title": "Dev",
            "country": "India",
            "salary": 10000,
        },
    )
    client.post(
        "/employees/",
        json={"full_name": "B", "job_title": "Dev", "country": "US", "salary": 20000},
    )
    client.post(
        "/employees/",
        json={
            "full_name": "C",
            "job_title": "Manager",
            "country": "India",
            "salary": 30000,
        },
    )

    resp_country = client.get("/metrics/country/India")
    assert resp_country.json()["avg"] == 20000

    resp_job = client.get("/metrics/job-title/Dev")
    assert resp_job.status_code == 200
    assert resp_job.json()["average_salary"] == 15000
