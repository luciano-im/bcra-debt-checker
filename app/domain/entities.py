from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Generic, TypeVar

from app.domain.enums import RequestStatus, RequestType
from app.domain.value_objects import (
    CUIT,
    DebtCheckRequestId,
    EmailAddress,
    UserId,
    ValueObject,
)

T = TypeVar("T", bound=ValueObject)


@dataclass(eq=False)
class Entity(Generic[T], ABC):
    """Base class for all entities in the domain model."""

    id_: T

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "id_" and getattr(self, "id_", None) is not None:
            raise ValueError("Cannot change the ID of an entity")
        super().__setattr__(name, value)

    def __eq__(self, other: Any) -> bool:
        return type(self) is type(other) and self.id_ == other.id_

    def __hash__(self) -> int:
        return hash((type(self), self.id_))


@dataclass(eq=False)
class PersonaFisicaJuridica(Entity[CUIT]):
    nombre: str
    cuit: CUIT


@dataclass(eq=False)
class DebtCheckRequest(Entity[DebtCheckRequestId]):
    cuit: CUIT
    timestamp: datetime
    request_type: RequestType
    response_time: int
    status: RequestStatus
    content: str


@dataclass(eq=False)
class User(Entity[UserId]):
    email: EmailAddress
    name: str
