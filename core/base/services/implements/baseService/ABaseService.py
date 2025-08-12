from abc import ABC
from typing import TypeVar, List, Optional, Dict, Any
from core.base.services.interfaces.IBaseService import IBaseService
from core.base.repositories.interfaces.IBaseRepository import IBaseRepository

T = TypeVar("T")


class ABaseService(IBaseService[T], ABC):
    """Implementación base abstracta del servicio."""

    def __init__(self, repository: IBaseRepository[T]):
        self.repository = repository

    def list(self) -> List[T]:
        return self.repository.get_all()

    def get(self, id: int) -> Optional[T]:
        return self.repository.get_by_id(id)

    def create(self, data: Dict[str, Any]) -> T:
        return self.repository.create(data)

    def update(self, id: int, data: Dict[str, Any]) -> T:
        instance = self.get(id)
        if instance is None:
            raise ValueError(f"Instancia con id {id} no encontrada")
        for key, value in data.items():
            if value in [None, ""]:
                raise ValueError(f"El campo '{key}' no puede estar vacío")
            setattr(instance, key, value)
        return self.repository.update(instance)

    def partial_update(self, id: int, data: Dict[str, Any]) -> T:
        instance = self.get(id)
        if instance is None:
            raise ValueError(f"Instancia con id {id} no encontrada")
        for key, value in data.items():
            if value not in [None, ""]:
                setattr(instance, key, value)
        return self.repository.update(instance)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
