from fastapi.testclient import TestClient

from app.main import app, repository

client = TestClient(app)


def setup_function() -> None:
    repository._pets.clear()  # noqa: SLF001
    repository._next_id = 1  # noqa: SLF001


def test_healthcheck() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    body = response.json()
    assert body['service'] == 'petsy'
    assert body['status'] == 'ok'


def test_full_pet_crud_flow() -> None:
    create = client.post(
        '/pets',
        json={
            'name': 'Milo',
            'pet_type': 'cat',
            'age': 3,
            'vaccinated': True,
            'owner_name': 'Anna',
        },
    )
    assert create.status_code == 201
    pet_id = create.json()['id']

    get_one = client.get(f'/pets/{pet_id}')
    assert get_one.status_code == 200
    assert get_one.json()['name'] == 'Milo'

    patch = client.patch(f'/pets/{pet_id}', json={'age': 4, 'vaccinated': False})
    assert patch.status_code == 200
    assert patch.json()['age'] == 4
    assert patch.json()['vaccinated'] is False

    list_filtered = client.get('/pets', params={'pet_type': 'cat', 'vaccinated': False})
    assert list_filtered.status_code == 200
    assert len(list_filtered.json()) == 1

    delete = client.delete(f'/pets/{pet_id}')
    assert delete.status_code == 204

    missing = client.get(f'/pets/{pet_id}')
    assert missing.status_code == 404


def test_validation_for_pet_type() -> None:
    response = client.post(
        '/pets',
        json={
            'name': 'Rex',
            'pet_type': 'dinosaur',
            'age': 5,
            'owner_name': 'Bob',
        },
    )
    assert response.status_code == 422
