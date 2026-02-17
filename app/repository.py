from datetime import datetime, UTC

from app.models import Pet, PetCreate, PetUpdate


class PetRepository:
    def __init__(self) -> None:
        self._pets: dict[int, Pet] = {}
        self._next_id = 1

    def list(self, *, pet_type: str | None = None, vaccinated: bool | None = None) -> list[Pet]:
        pets = list(self._pets.values())
        if pet_type is not None:
            pets = [pet for pet in pets if pet.pet_type == pet_type]
        if vaccinated is not None:
            pets = [pet for pet in pets if pet.vaccinated is vaccinated]
        return sorted(pets, key=lambda pet: pet.id)

    def get(self, pet_id: int) -> Pet | None:
        return self._pets.get(pet_id)

    def create(self, payload: PetCreate) -> Pet:
        pet = Pet(
            id=self._next_id,
            created_at=datetime.now(UTC),
            **payload.model_dump(),
        )
        self._pets[self._next_id] = pet
        self._next_id += 1
        return pet

    def update(self, pet_id: int, payload: PetUpdate) -> Pet | None:
        pet = self._pets.get(pet_id)
        if pet is None:
            return None

        updates = payload.model_dump(exclude_unset=True)
        updated = pet.model_copy(update=updates)
        self._pets[pet_id] = updated
        return updated

    def delete(self, pet_id: int) -> bool:
        return self._pets.pop(pet_id, None) is not None
