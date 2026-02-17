from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PetType = Literal["dog", "cat", "bird", "rodent", "other"]


class PetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    pet_type: PetType
    age: int = Field(ge=0, le=100)
    vaccinated: bool = False
    owner_name: str = Field(min_length=1, max_length=100)


class PetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    pet_type: PetType | None = None
    age: int | None = Field(default=None, ge=0, le=100)
    vaccinated: bool | None = None
    owner_name: str | None = Field(default=None, min_length=1, max_length=100)


class Pet(PetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ErrorResponse(BaseModel):
    detail: str


class ServiceInfo(BaseModel):
    service: str
    status: str
    date: date
