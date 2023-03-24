import pytest
from fastapi.testclient import TestClient
from main import api
from functions import get_price_history_from_db

client = TestClient(api)


# Test the add_user endpoint
def test_add_user():
    new_user = {
        "id_api_users": 1,
        "name": "John",
        "lastname": "Doe",
        "login": "johndoe",
        "password": "password123",
        "validity_day": 180,
    }
    response = client.post(
        "/add_user/1/John/Doe/johndoe/password123", auth=("htemp123", "temp123")
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "User added successfully",
        "name": "John",
        "lastname": "Doe",
        "login": "johndoe",
        "password": "password123",
    }


# Test the update_user endpoint
def test_update_user():
    updated_user = {
        "id_api_users": 1,
        "name": "Jane",
        "lastname": "Doe",
        "login": "janedoe",
        "password": "newpassword",
        "validity_day": 180,
    }
    response = client.put(
        "/users/1/Jane/Doe/janedoe/newpassword", auth=("htemp123", "temp123")
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "User updated successfully",
        "name": "Jane",
        "lastname": "Doe",
        "login": "janedoe",
        "password": "newpassword",
    }


# Test the delete_user endpoint
def test_delete_user():
    response = client.delete("/users/1", auth=("htemp123", "temp123"))
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}


def test_predict_close_price():
    response = client.get("/predict", auth=("htemp123", "temp123"))
    assert response.status_code == 200
    assert "predicted_close_price" in response.json()
    assert "decision" in response.json()


def test_get_price_history():
    start_time = "2023-02-01 00:00:00"
    end_time = "2023-02-28 23:59:59"
    interval = "1H"
    response = client.get(
        f"/price_history/{start_time}/{end_time}/{interval}/BTC",
        auth=("htemp123", "temp123"),
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_add_user():
    new_user = {"username": "test_user", "password": "test_password"}
    response = client.post("/add_user", json=new_user, auth=("htemp123", "temp123"))
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_get_model_performance():
    response = client.get("/model_performance", auth=("htemp123", "temp123"))
    assert response.status_code == 200
    assert "model_performance" in response.json()
    assert "mean_absolute_error" in response.json()["model_performance"]


@pytest.mark.parametrize(
    "start_time, end_time, interval, symbol",
    [
        ("2023-02-01 00:00:00", "2023-02-28 23:59:59", "7D", "BTC"),
        ("2023-02-01 00:00:00", "2023-02-28 23:59:59", "1D", "BTC"),
    ],
)
def test_get_price_history_from_db(start_time, end_time, interval, symbol):
    price_history = get_price_history_from_db(start_time, end_time, interval, symbol)
    assert len(price_history) > 0
    assert "price" in price_history[0]
    assert "date" in price_history[0]
    assert "symbol" in price_history[0]
    assert "interval" in price_history[0]
