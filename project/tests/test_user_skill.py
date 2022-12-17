import json

from app import constant

years_of_experience = 4
endpoint = "/user_skills/"
payload = dict(user_id="", skill_id="", years_of_experience=years_of_experience)
wrong_user_skill_id = "40fe45f4-8285-424f-aa1a-554a322e7ba0"


def __add_user_and_skill(test_app_with_db):
    user_response = test_app_with_db.post(
        "/users/",
        data=json.dumps(
            {
                "first_name": "Elon",
                "last_name": "Musk",
                "email": "elon.musk@gmail.com",
                "years_of_experience": 5,
            }
        ),
    )
    payload["user_id"] = user_response.json()["id"]

    skill_response = test_app_with_db.post(
        "/skills/", data=json.dumps({"name": "Python"})
    )
    payload["skill_id"] = skill_response.json()["id"]


def test_read_user_skill(test_app_with_db):
    __add_user_and_skill(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_skill_id = response.json()["id"]

    response = test_app_with_db.get(f"{endpoint}{user_skill_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == user_skill_id
    assert response_dict["years_of_experience"] == years_of_experience


def test_read_user_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.get(f"{endpoint}{wrong_user_skill_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.USER_SKILL_NOT_FOUND


def test_create_user_skill(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))

    assert response.status_code == 201
    assert response.json()["years_of_experience"] == years_of_experience


def test_create_user_skills_invalid_json(test_app):
    response = test_app.post(endpoint, data=json.dumps({}))
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "user_id"],
        "msg": "field required",
        "type": "value_error.missing",
    }


def test_read_all_user_skills(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_skill_id = response.json()["id"]

    response = test_app_with_db.get(endpoint)
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == user_skill_id, response_list))) == 1


def test_remove_user_skill(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_skill_id = response.json()["id"]

    response = test_app_with_db.delete(f"{endpoint}{user_skill_id}/")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == user_skill_id
    assert response_dict["years_of_experience"] == years_of_experience


def test_remove_user_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete(f"{endpoint}{wrong_user_skill_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.USER_SKILL_NOT_FOUND


def test_update_user_skill(test_app_with_db):
    __add_user_and_skill(test_app_with_db)
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_skill_id = response.json()["id"]

    years_of_experience = 4
    payload["years_of_experience"] = years_of_experience
    response = test_app_with_db.put(
        f"{endpoint}{user_skill_id}/", data=json.dumps(payload)
    )
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == user_skill_id
    assert response_dict["years_of_experience"] == years_of_experience


def test_update_user_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        f"{endpoint}{wrong_user_skill_id}/", data=json.dumps(payload)
    )
    assert response.status_code == 404
    assert response.json()["detail"] == constant.USER_SKILL_NOT_FOUND


def test_update_user_skill_invalid_json(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_skill_id = response.json()["id"]

    response = test_app_with_db.put(f"{endpoint}{user_skill_id}/", data=json.dumps({}))
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "user_id"],
        "msg": "field required",
        "type": "value_error.missing",
    }


def test_update_user_skill_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{summary_id}/", data=json.dumps({"url": "https://foo.bar"})
    )
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "user_id"],
        "msg": "field required",
        "type": "value_error.missing",
    }
