import json

from app import constant

years_of_experience = 4
endpoint = "/job_offer_skills/"
payload = dict(job_offer_id="", skill_id="", years_of_experience=years_of_experience)
wrong_job_offer_skill_id = "40fe45f4-8285-424f-aa1a-554a322e7ba0"


def __add_job_offer_and_skill(test_app_with_db):
    company_response = test_app_with_db.post(
        "/companies/", data=json.dumps({"name": "Hunty"})
    )
    company_id = company_response.json()["id"]

    job_offer_response = test_app_with_db.post(
        "/job_offers/",
        data=json.dumps(
            {
                "name": "Python Developer",
                "currency": "USD",
                "salary": 2000,
                "url": "https://findjob.com/jobid/1020/",
                "company_id": company_id,
            }
        ),
    )
    payload["job_offer_id"] = job_offer_response.json()["id"]

    skill_response = test_app_with_db.post(
        "/skills/", data=json.dumps({"name": "Python"})
    )
    payload["skill_id"] = skill_response.json()["id"]


def test_read_job_offer_skill(test_app_with_db):
    __add_job_offer_and_skill(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_skill_id = response.json()["id"]

    response = test_app_with_db.get(f"{endpoint}{job_offer_skill_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == job_offer_skill_id
    assert response_dict["years_of_experience"] == years_of_experience


def test_read_job_offer_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.get(f"{endpoint}{wrong_job_offer_skill_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.JOB_OFFER_SKILL_NOT_FOUND


def test_create_job_offer_skill(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))

    assert response.status_code == 201
    assert response.json()["years_of_experience"] == years_of_experience


def test_create_job_offer_skills_invalid_json(test_app):
    response = test_app.post(endpoint, data=json.dumps({}))
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "job_offer_id"],
        "msg": "field required",
        "type": "value_error.missing",
    }


def test_read_all_job_offer_skills(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_skill_id = response.json()["id"]

    response = test_app_with_db.get(endpoint)
    assert response.status_code == 200

    response_list = response.json()
    assert (
        len(list(filter(lambda d: d["id"] == job_offer_skill_id, response_list))) == 1
    )


def test_remove_job_offer_skill(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_skill_id = response.json()["id"]

    response = test_app_with_db.delete(f"{endpoint}{job_offer_skill_id}/")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == job_offer_skill_id
    assert response_dict["years_of_experience"] == years_of_experience


def test_remove_job_offer_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete(f"{endpoint}{wrong_job_offer_skill_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.JOB_OFFER_SKILL_NOT_FOUND


def test_update_job_offer_skill(test_app_with_db):
    __add_job_offer_and_skill(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_skill_id = response.json()["id"]

    years_of_experience = 4
    payload["years_of_experience"] = years_of_experience
    response = test_app_with_db.put(
        f"{endpoint}{job_offer_skill_id}/", data=json.dumps(payload)
    )
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == job_offer_skill_id
    assert response_dict["years_of_experience"] == years_of_experience


def test_update_job_offer_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        f"{endpoint}{wrong_job_offer_skill_id}/", data=json.dumps(payload)
    )
    assert response.status_code == 404
    assert response.json()["detail"] == constant.JOB_OFFER_SKILL_NOT_FOUND


def test_update_job_offer_skill_invalid_json(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    job_offer_skill_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{job_offer_skill_id}/", data=json.dumps({})
    )
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "job_offer_id"],
        "msg": "field required",
        "type": "value_error.missing",
    }


def test_update_job_offer_skill_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{summary_id}/", data=json.dumps({"url": "https://foo.bar"})
    )
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "job_offer_id"],
        "msg": "field required",
        "type": "value_error.missing",
    }
