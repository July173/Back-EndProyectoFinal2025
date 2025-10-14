from core.base.repositories.interfaces.IBaseRepository import IBaseRepository
from typing import List, Optional, TypeVar
from django.db import models

T = TypeVar("T", bound=models.Model)

class BaseRepository(IBaseRepository[T]):

    def __init__(self, model: type[T]):
        self.model = model

    def get_queryset(self):
        # Returns all records, without filtering by delete_at or active
        return self.model.objects.all()

    def get_all(self) -> List[T]:
        """Gets all records from the model."""
        return list(self.get_queryset())

    def get_by_id(self, id: int) -> Optional[T]:
        """Gets a record by its ID."""
        return self.get_queryset().filter(pk=id).first()

    def create(self, data: dict) -> T:
        """Creates a new record with the given data."""
        instance = self.model.objects.create(**data)
        return instance

    def update(self, entity: T) -> T:
        """Saves changes to an existing instance (PUT)."""
        entity.save()
        return entity

    def partial_update(self, entity: T, data: dict) -> T:
        """Partially updates fields of an existing instance (PATCH)."""
        for attr, value in data.items():
            setattr(entity, attr, value)
        entity.save()
        return entity

    def delete(self, id: int) -> bool:
        """Physically deletes a record by ID."""
        instance = self.model.objects.filter(pk=id).first()
        if instance:
            instance.delete()
            return True
        return False

    def soft_delete(self, id: int) -> bool:
        """Performs logical deletion (changes active and delete_at)."""
        instance = self.model.objects.filter(pk=id).first()
        if instance and hasattr(instance, 'active') and hasattr(instance, 'delete_at'):
            from django.utils import timezone
            if instance.active:
                instance.active = False
                instance.delete_at = timezone.now()
            else:
                instance.active = True
                instance.delete_at = None
            instance.save()
            return True
        return False