import allure
import pytest
allure.epic("API Testing")
@allure.feature("Checking httpbin GET endpoints")
@allure.story("GET /get echoes query params")
@pytest.mark.api
def test_get_echoes_args(api):
    with allure.step("Send GET /get?hello=world"):
        resp = api.get("/get", params={"hello": "world"})

    with allure.step("Validate response"):
        assert resp.status_code == 200
        data = resp.json()
        assert data["args"]["hello"] == "world"
