from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from app.main import app, repository
from app.models import PetCreate

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


def test_patch_rejects_null_required_field() -> None:
    create = client.post(
        '/pets',
        json={
            'name': 'Bella',
            'pet_type': 'dog',
            'age': 5,
            'vaccinated': True,
            'owner_name': 'Liam',
        },
    )
    pet_id = create.json()['id']

    patch = client.patch(f'/pets/{pet_id}', json={'name': None})
    assert patch.status_code == 422

    unchanged = client.get(f'/pets/{pet_id}')
    assert unchanged.status_code == 200
    assert unchanged.json()['name'] == 'Bella'


def test_repository_create_assigns_unique_ids_under_concurrency() -> None:
    payload = PetCreate(name='Nori', pet_type='cat', age=2, vaccinated=False, owner_name='Eve')

    with ThreadPoolExecutor(max_workers=20) as executor:
        pets = list(executor.map(lambda _: repository.create(payload), range(50)))

    ids = [pet.id for pet in pets]
    assert len(ids) == len(set(ids))
    assert len(repository._pets) == 50  # noqa: SLF001
