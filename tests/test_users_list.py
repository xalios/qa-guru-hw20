import requests
import os
import json
from jsonschema.validators import validate


def load_json_schema(name: str):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schemas', name)
    with open(schema_path) as schema:
        return json.loads(schema.read())


def test_users_smoke():
    request = requests.get('https://reqres.in/api/users')

    assert request.status_code == 200


def test_users_schema():
    schema = load_json_schema('users_list.json')

    request = requests.get('https://reqres.in/api/users')

    validate(request.json(), schema=schema)


def test_users_per_page():
    request = requests.get('https://reqres.in/api/users', params={'per_page': 3})

    assert request.json()['per_page'] == 3


def test_users_pagination():
    request = requests.get('https://reqres.in/api/users', params={'page': 2})

    assert request.json()['page'] == 2
    assert request.json()['data'][0]['id'] == 7


