import pytest
from fastapi.testclient import TestClient
from main import api
from functions import *


client = TestClient(api)


def test_add_user():
    
    response = client.post(
        "/add_user/1000",
        auth=("hennaji", "temp123"),
        json={
            "name": "John",
            "lastname": "Doe",
            "login": "johndoe",
            "password": "password123",
        },
        
    )

    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert response.json() == {
        "message": "User added successfully",
        "name": "John",
        "lastname": "Doe",
        "login": "johndoe",
        "password": "password123",
    }
    cnx.close()



def test_update_user():
    response = client.put(
        "/users/1000",
        auth=("hennaji", "temp123"),
        json={
            "name": "John",
            "lastname": "Smith",
            "login": "johnsmith",
            "password": "password123",
        },
        
    )
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert response.json() == {
        "message": "User updated successfully",
        "name": "John",
        "lastname": "Smith",
        "login": "johnsmith",
        "password": "password123",
    }
    cnx.close()



def test_delete_user():
    response = client.delete("/users/1000", auth=("hennaji", "temp123"))
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert response.json() == {"message": "User deleted successfully"}
    cnx.close()



def test_predict_close_price():
    response = client.get("/predict", auth=("hennaji", "temp123"))
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert "predicted_close_price" in response.json()
    assert "decision" in response.json()


def test_get_price_history():
    start_time = "2023-02-01 00:00:00"
    end_time = "2023-02-28 23:59:59"
    interval = "1H"
    response = client.get(
        f"/price_history/{start_time}/{end_time}/{interval}/BTC",
        auth=("hennaji", "temp123"),
    )
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    assert len(response.json()) > 0


def test_get_model_performance():
    response = client.get("/model_performance", auth=("hennaji", "temp123"))
    assert response.status_code == 200, f"Unexpected response: {response.json()}"
    result = response.json()
    assert "model_performance" in result
    performance_metrics = result["model_performance"]
    assert "mean_absolute_error" in performance_metrics
    assert "mean_squared_error" in performance_metrics
    assert "root_mean_squared_error" in performance_metrics
    assert "r2_score" in performance_metrics


# def test_retrain_model():
#     response = client.post("/retrain_model", auth=("hennaji", "temp123"))
#     assert response.status_code == 200
#     result = response.json()
#     assert result == {"message": "Le modèle a été réentraîné avec succès."}
