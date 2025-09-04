from core.base.repositories.implements.baseRepository.ABaseRepository import ABaseRepository
from typing import List, Optional, TypeVar
from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseRepository(ABaseRepository[T]):
    """Implementación concreta del repositorio con funcionalidades extendidas."""

    def get_queryset(self):
        qs = self.model.objects.all()
        if hasattr(self.model, 'delete_at'):
            qs = qs.filter(delete_at=None)
        return qs

    def get_all(self) -> List[T]:
        return list(self.get_queryset())

    def get_by_id(self, id: int) -> Optional[T]:
        return self.get_queryset().filter(pk=id).first()

    def create(self, data: dict) -> T:
        """Crea una instancia del modelo usando datos validados."""
        instance = self.model.objects.create(**data)
        return instance

    def delete(self, id: int) -> bool:
        return super().delete(id)

    def soft_delete(self, id: int) -> bool:
        return super().soft_delete(id)
