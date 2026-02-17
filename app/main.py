from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status

from app.models import ErrorResponse, Pet, PetCreate, PetType, PetUpdate, ServiceInfo
from app.repository import PetRepository

app = FastAPI(
    title="Petsy API",
    description="Simple pet management service",
    version="0.1.0",
)

repository = PetRepository()


def get_repository() -> PetRepository:
    return repository


@app.get("/health", response_model=ServiceInfo, tags=["system"])
def healthcheck() -> ServiceInfo:
    return ServiceInfo(service="petsy", status="ok", date=date.today())


@app.get("/pets", response_model=list[Pet], tags=["pets"])
def list_pets(
    pet_type: Annotated[PetType | None, Query()] = None,
    vaccinated: Annotated[bool | None, Query()] = None,
    repo: PetRepository = Depends(get_repository),
) -> list[Pet]:
    return repo.list(pet_type=pet_type, vaccinated=vaccinated)


@app.post(
    "/pets",
    response_model=Pet,
    status_code=status.HTTP_201_CREATED,
    responses={422: {"model": ErrorResponse}},
    tags=["pets"],
)
def create_pet(payload: PetCreate, repo: PetRepository = Depends(get_repository)) -> Pet:
    return repo.create(payload)


@app.get(
    "/pets/{pet_id}",
    response_model=Pet,
    responses={404: {"model": ErrorResponse}},
    tags=["pets"],
)
def get_pet(pet_id: int, repo: PetRepository = Depends(get_repository)) -> Pet:
    pet = repo.get(pet_id)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet


@app.patch(
    "/pets/{pet_id}",
    response_model=Pet,
    responses={404: {"model": ErrorResponse}},
    tags=["pets"],
)
def update_pet(pet_id: int, payload: PetUpdate, repo: PetRepository = Depends(get_repository)) -> Pet:
    pet = repo.update(pet_id, payload)
    if pet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet


@app.delete(
    "/pets/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
    tags=["pets"],
)
def delete_pet(pet_id: int, repo: PetRepository = Depends(get_repository)) -> None:
    deleted = repo.delete(pet_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
