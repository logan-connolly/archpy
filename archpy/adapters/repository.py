import dataclasses
from typing import Generic, Type, TypeVar

from sqlalchemy.orm import Session

DomainObject = TypeVar("DomainObject")


@dataclasses.dataclass
class Repository(Generic[DomainObject]):
    session: Session
    model: Type[DomainObject]

    def add(self, obj: DomainObject) -> None:
        self.session.add(obj)

    def get(self, reference) -> Type[DomainObject]:
        return self.session.query(self.model).filter_by(reference=reference).one()

    def list(self) -> list[Type[DomainObject]]:
        return self.session.query(self.model).all()
