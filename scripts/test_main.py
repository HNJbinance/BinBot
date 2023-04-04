from main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_predict_close_price():
    response = client.get("/predict")
    assert response.status_code == 200
    json_response = response.json()
    assert "symbol" in json_response
    assert "interval" in json_response
    assert "actual_time" in json_response
    assert "actual_price" in json_response
    assert "next_hour" in json_response
    assert "predicted_close_price" in json_response
    assert "decision" in json_response
    assert isinstance(json_response["symbol"], str)
    assert isinstance(json_response["interval"], str)
    assert isinstance(json_response["actual_time"], str)
    assert isinstance(json_response["actual_price"], float)
    assert isinstance(json_response["next_hour"], str)
    assert isinstance(json_response["predicted_close_price"], float)
    assert isinstance(json_response["decision"], str)
