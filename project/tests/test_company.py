import json

from app import constant

company_name = "Hunty"
endpoint = "/companies/"
payload = dict(name=company_name)
wrong_company_id = "40fe45f4-8285-424f-aa1a-554a322e7ba0"


def test_read_company(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    company_id = response.json()["id"]

    response = test_app_with_db.get(f"{endpoint}{company_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == company_id
    assert response_dict["name"] == company_name


def test_read_company_incorrect_id(test_app_with_db):
    response = test_app_with_db.get(f"{endpoint}{wrong_company_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.COMPANY_NOT_FOUND


def test_create_company(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))

    assert response.status_code == 201
    assert response.json()["name"] == company_name


def test_create_companies_invalid_json(test_app):
    response = test_app.post(endpoint, data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_read_all_companies(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    company_id = response.json()["id"]

    response = test_app_with_db.get(endpoint)
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == company_id, response_list))) == 1


def test_remove_company(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    company_id = response.json()["id"]

    response = test_app_with_db.delete(f"{endpoint}{company_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": company_id, "name": company_name}


def test_remove_company_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete(f"{endpoint}{wrong_company_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.COMPANY_NOT_FOUND


def test_update_company(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    company_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{company_id}/", data=json.dumps({"name": "new_name"})
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == company_id
    assert response_dict["name"] == "new_name"


def test_update_company_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        f"{endpoint}{wrong_company_id}/", data=json.dumps({"name": "new_name"})
    )
    assert response.status_code == 404
    assert response.json()["detail"] == constant.COMPANY_NOT_FOUND


def test_update_company_invalid_json(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    company_id = response.json()["id"]

    response = test_app_with_db.put(f"{endpoint}{company_id}/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_update_company_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{summary_id}/", data=json.dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
