import pytest
from fastapi.testclient import TestClient
from main import api, get_price_history_from_db

client = TestClient(api)

def test_predict_close_price():
    response = client.get("/predict", auth=("ilham", "noumir"))
    assert response.status_code == 200
    assert "predicted_close_price" in response.json()
    assert "decision" in response.json()

def test_get_price_history():
    start_time = "2023-02-01 00:00:00"
    end_time = "2023-02-28 23:59:59"
    interval = "7D"
    response = client.get(f"/price_history/{start_time}/{end_time}/{interval}/BTC", auth=("ilham", "noumir"))
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_add_user():
    new_user = {"username": "test_user", "password": "test_password"}
    response = client.post("/add_user", json=new_user, auth=("ilham", "noumir"))
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_get_model_performance():
    response = client.get("/model_performance", auth=("ilham", "noumir"))
    assert response.status_code == 200
    assert "model_performance" in response.json()
    assert "mean_absolute_error" in response.json()["model_performance"]

@pytest.mark.parametrize("start_time, end_time, interval, symbol", [
    ("2023-02-01 00:00:00", "2023-02-28 23:59:59", "7D", "BTC"),
    ("2023-02-01 00:00:00", "2023-02-28 23:59:59", "1D", "BTC"),
])
def test_get_price_history_from_db(start_time, end_time, interval, symbol):
    price_history = get_price_history_from_db(start_time, end_time, interval, symbol)
    assert len(price_history) > 0
    assert "price" in price_history[0]
    assert "date" in price_history[0]
    assert "symbol" in price_history[0]
    assert "interval" in price_history[0]

