import json

from app import constant

first_name = "Elon"
endpoint = "/users/"
payload = dict(
    first_name=first_name,
    last_name="Musk",
    email="elon.musk@gmail.com",
    years_of_experience=6,
)
wrong_user_id = "40fe45f4-8285-424f-aa1a-554a322e7ba0"


def test_read_user(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_id = response.json()["id"]

    response = test_app_with_db.get(f"{endpoint}{user_id}/")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == user_id
    assert response_dict["first_name"] == first_name


def test_read_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.get(f"{endpoint}{wrong_user_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.USER_NOT_FOUND


def test_create_user(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))

    assert response.status_code == 201
    assert response.json()["first_name"] == first_name


def test_create_users_invalid_json(test_app):
    response = test_app.post(endpoint, data=json.dumps({}))
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "first_name"],
        "msg": "field required",
        "type": "value_error.missing",
    }


def test_read_all_users(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_id = response.json()["id"]

    response = test_app_with_db.get(endpoint)
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == user_id, response_list))) == 1


def test_remove_user(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_id = response.json()["id"]

    response = test_app_with_db.delete(f"{endpoint}{user_id}/")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == user_id
    assert response_dict["first_name"] == first_name


def test_remove_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete(f"{endpoint}{wrong_user_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == constant.USER_NOT_FOUND


def test_update_user(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_id = response.json()["id"]

    new_name = "Mark"
    payload["first_name"] = new_name
    response = test_app_with_db.put(f"{endpoint}{user_id}/", data=json.dumps(payload))
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == user_id
    assert response_dict["first_name"] == new_name


def test_update_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        f"{endpoint}{wrong_user_id}/", data=json.dumps(payload)
    )
    assert response.status_code == 404
    assert response.json()["detail"] == constant.USER_NOT_FOUND


def test_update_user_invalid_json(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    user_id = response.json()["id"]

    response = test_app_with_db.put(f"{endpoint}{user_id}/", data=json.dumps({}))
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "first_name"],
        "msg": "field required",
        "type": "value_error.missing",
    }


def test_update_user_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(endpoint, data=json.dumps(payload))
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{endpoint}{summary_id}/", data=json.dumps({"url": "https://foo.bar"})
    )
    response_dict = response.json()

    assert response.status_code == 422
    assert response_dict["detail"][0] == {
        "loc": ["body", "first_name"],
        "msg": "field required",
        "type": "value_error.missing",
    }
