import requests
import os
import json
from jsonschema.validators import validate


def load_json_schema(name: str):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schemas', name)
    with open(schema_path) as schema:
        return json.loads(schema.read())


def test_users_smoke():
    request = requests.get('https://reqres.in/api/users/1')

    assert request.status_code == 200


def test_users_single_schema():
    schema = load_json_schema('users_single.json')

    request = requests.get('https://reqres.in/api/users/1')

    validate(request.json(), schema=schema)


def test_users_single_id():
    request = requests.get('https://reqres.in/api/users/2')

    assert request.json()['data']['id'] == 2


def test_create_user():
    request = requests.post(
        url='https://reqres.in/api/users',
        data={'name': 'Bob', 'job': 'QA'}
    )

    assert request.status_code == 201
    assert request.json()['name'] == 'Bob'
    assert request.json()['job'] == 'QA'
    assert 'id' in request.json()
    assert 'createdAt' in request.json()


def test_edit_user():
    request = requests.patch(
        url='https://reqres.in/api/users/37',
        data={'name': 'Bill'}
    )

    assert request.status_code == 200
    assert request.json()['name'] == 'Bill'


def test_delete_user():
    request = requests.delete(url='https://reqres.in/api/users/2')

    assert request.status_code == 204
    assert request.text == ''
