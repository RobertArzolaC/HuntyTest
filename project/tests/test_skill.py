import json

from app import constant

skill_name = "Python"
endpoint = "/skills/"
payload = dict(name=skill_name)
wrong_skill_id = "40fe45f4-8285-424f-aa1a-554a322e7ba0"


def test_read_skill(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    skill_id = response.json()["id"]

    response = test_app_with_db.get(f"{endpoint}{skill_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == skill_id
    assert response_dict["name"] == skill_name


def test_read_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.get(f"{endpoint}{wrong_skill_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.SKILL_NOT_FOUND


def test_create_skill(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))

    assert response.status_code == 201
    assert response.json()["name"] == skill_name


def test_create_skills_invalid_json(test_app):
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


def test_read_all_skills(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    skill_id = response.json()["id"]

    response = test_app_with_db.get(endpoint)
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == skill_id, response_list))) == 1


def test_remove_skill(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    skill_id = response.json()["id"]

    response = test_app_with_db.delete(f"{endpoint}{skill_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": skill_id, "name": skill_name}


def test_remove_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete(f"{endpoint}{wrong_skill_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.SKILL_NOT_FOUND


def test_update_skill(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    skill_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{skill_id}/", data=json.dumps({"name": "new_name"})
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == skill_id
    assert response_dict["name"] == "new_name"


def test_update_skill_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        f"{endpoint}{wrong_skill_id}/", data=json.dumps({"name": "new_name"})
    )
    assert response.status_code == 404
    assert response.json()["detail"] == constant.SKILL_NOT_FOUND


def test_update_skill_invalid_json(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    skill_id = response.json()["id"]

    response = test_app_with_db.put(f"{endpoint}{skill_id}/", data=json.dumps({}))
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


def test_update_skill_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    skill_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{skill_id}/", data=json.dumps({"url": "https://foo.bar"})
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
