from django.utils import timezone
from core.base.repositories.implements.baseRepository.ABaseRepository import ABaseRepository
from typing import List, Optional, TypeVar
from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseRepository(ABaseRepository[T]):
    """Implementación concreta del repositorio con funcionalidades extendidas."""

    def get_queryset(self):
        qs = self.model.objects.all()
        if hasattr(self.model, 'is_deleted'):
            qs = qs.filter(is_deleted=False)
        return qs

    def get_all(self) -> List[T]:
        return list(self.get_queryset())

    def get_by_id(self, id: int) -> Optional[T]:
        return self.get_queryset().filter(pk=id).first()

    def persistential_delete(self, instance: T) -> T:
        """Eliminación persistencial: desactiva el registro y guarda la fecha."""
        # Manejo de campos de estado
        if hasattr(instance, 'active'):
            instance.active = False
        elif hasattr(instance, 'is_active'):
            instance.is_active = False
        elif hasattr(instance, 'is_deleted'):
            instance.is_deleted = True
        elif hasattr(instance, 'deleted'):
            instance.deleted = True

        # Manejo de campos de fecha
        current_time = timezone.now()
        if hasattr(instance, 'delete_at'):
            instance.delete_at = current_time
        elif hasattr(instance, 'deleted_at'):
            instance.deleted_at = current_time
        elif hasattr(instance, 'date_deleted'):
            instance.date_deleted = current_time

        instance.save()
        return instance

    def logical_delete(self, instance: T) -> Optional[T]:
        """Eliminación lógica: puede activar o desactivar según el estado actual."""
        if hasattr(instance, 'active'):
            instance.active = not instance.active
        elif hasattr(instance, 'is_active'):
            instance.is_active = not instance.is_active
        elif hasattr(instance, 'is_deleted'):
            instance.is_deleted = not instance.is_deleted
        elif hasattr(instance, 'deleted'):
            instance.deleted = not instance.deleted
        else:
            return super().delete(instance.pk)

        instance.save()
        return instance

    def delete(self, id: int) -> bool:
        """Eliminación física permanente."""
        return super().delete(id)

    def create(self, data: dict) -> T:
        """Crea una instancia del modelo usando datos validados."""
        instance = self.model.objects.create(**data)
        return instance
