# tests/test_main.py

from src.data_collection import DataCollector
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AIDSCRO API"}


def test_get_data():
    response = client.get("/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_predict():
    input_data = {
        "hour": 12,
        "day_of_week": 2,
        "traffic_density": 0.5,
        "air_quality_index": 100,
        "waste_generated": 50,
        "water_consumption": 3000
    }
    response = client.post("/predict", json=input_data)
    assert response.status_code == 200
    assert "predicted_energy_consumption" in response.json()


def test_collect_data():
    new_data = {
        "energy_consumption": 250.5,
        "traffic_density": 0.7,
        "air_quality_index": 120,
        "waste_generated": 45.5,
        "water_consumption": 2800
    }
    response = client.post("/collect", params=new_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Data collected successfully"}
