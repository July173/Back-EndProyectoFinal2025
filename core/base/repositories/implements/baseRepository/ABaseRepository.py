from abc import ABC
from django.db import models
from typing import TypeVar, List, Optional
from core.base.repositories.interfaces.IBaseRepository import IBaseRepository

T = TypeVar("T", bound=models.Model)


class ABaseRepository(IBaseRepository[T], ABC):
    """Implementación base abstracta del repositorio."""

    def __init__(self, model: type[T]):
        self.model = model

    def get_all(self) -> List[T]:
        return list(self.model.objects.all())

    def get_by_id(self, id: int) -> Optional[T]:
        return self.model.objects.filter(pk=id).first()

    def create(self, data: dict) -> T:
        instance = self.model.objects.create(**data)
        return instance

    def update(self, entity: T) -> T:
        entity.save()
        return entity

    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj:
            obj.delete()  # Elimina físicamente el registro de la base de datos
            return True
        return False
