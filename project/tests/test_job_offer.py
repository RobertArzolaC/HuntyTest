import json

from app import constant

name = "Python Developer"
endpoint = "/job_offers/"
payload = dict(
    name=name,
    currency="USD",
    salary=3000,
    url="https://findjob.com/jobid/1020/",
)
wrong_job_offer_id = "40fe45f4-8285-424f-aa1a-554a322e7ba0"


def __add_company(test_app_with_db):
    response = test_app_with_db.post("/companies/", data=json.dumps({"name": "Hunty"}))
    payload["company_id"] = response.json()["id"]


def test_read_job_offer(test_app_with_db):
    __add_company(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_id = response.json()["id"]

    response = test_app_with_db.get(f"{endpoint}{job_offer_id}/")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == job_offer_id
    assert response_dict["name"] == name


def test_read_job_offer_incorrect_id(test_app_with_db):
    response = test_app_with_db.get(f"{endpoint}{wrong_job_offer_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.JOB_OFFER_NOT_FOUND


def test_create_job_offer(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))

    assert response.status_code == 201
    assert response.json()["name"] == name


def test_create_job_offers_invalid_json(test_app):
    response = test_app.post(endpoint, data=json.dumps({}))
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "name"],
        "msg": "field required",
        "type": "value_error.missing",
    }


def test_read_all_job_offers(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_id = response.json()["id"]

    response = test_app_with_db.get(endpoint)
    response_list = response.json()

    assert response.status_code == 200
    assert len(list(filter(lambda d: d["id"] == job_offer_id, response_list))) == 1


def test_remove_job_offer(test_app_with_db):
    __add_company(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_id = response.json()["id"]

    response = test_app_with_db.delete(f"{endpoint}{job_offer_id}/")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == job_offer_id
    assert response_dict["name"] == name


def test_remove_job_offer_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete(f"{endpoint}{wrong_job_offer_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.JOB_OFFER_NOT_FOUND


def test_update_job_offer(test_app_with_db):
    __add_company(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_id = response.json()["id"]

    new_name = "New Job"
    payload["name"] = new_name
    response = test_app_with_db.put(
        f"{endpoint}{job_offer_id}/", data=json.dumps(payload)
    )
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == job_offer_id
    assert response_dict["name"] == new_name


def test_update_job_offer_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        f"{endpoint}{wrong_job_offer_id}/", data=json.dumps(payload)
    )
    assert response.status_code == 404
    assert response.json()["detail"] == constant.JOB_OFFER_NOT_FOUND


def test_update_job_offer_invalid_json(test_app_with_db):
    __add_company(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_id = response.json()["id"]

    response = test_app_with_db.put(f"{endpoint}{job_offer_id}/", data=json.dumps({}))
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "name"],
        "msg": "field required",
        "type": "value_error.missing",
    }


def test_update_job_offer_invalid_keys(test_app_with_db):
    __add_company(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{job_offer_id}/", data=json.dumps({"link": "https://foo.bar"})
    )
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "name"],
        "msg": "field required",
        "type": "value_error.missing",
    }
