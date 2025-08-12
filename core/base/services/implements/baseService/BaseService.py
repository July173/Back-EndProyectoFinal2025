from datetime import timezone
from typing import TypeVar, Dict, Any, Optional
from core.base.services.implements.baseService.ABaseService import ABaseService
from core.base.repositories.interfaces.IBaseRepository import IBaseRepository

T = TypeVar("T")


class BaseService(ABaseService[T]):
    """Implementación concreta del servicio con funcionalidades extendidas."""

    def __init__(self, repository: IBaseRepository[T]):
        super().__init__(repository)

    def create(self, data: Dict[str, Any]) -> T:
        """Crea una nueva instancia a partir de los datos."""
        # Asumimos que el repositorio tiene un método create que acepta un
        # diccionario
        # Si no es así, deberíamos adaptar esta implementación
        return self.repository.create(data)

    def persistential_delete(self, id: int) -> Optional[T]:
        """
        Eliminación persistencial: desactiva el registro y guarda fecha.

        Returns:
            La instancia modificada o None si no se encontró
        """
        instance = self.get(id)
        if instance is None:
            return None

        if hasattr(instance, 'active'):
            instance.active = False
        elif hasattr(instance, 'is_active'):
            instance.is_active = False

        if hasattr(instance, 'deleted_at'):
            instance.deleted_at = timezone.now()

        return self.repository.update(instance)

    def logical_delete(self, id: int) -> Optional[T]:
        """
        Eliminación lógica: alterna el estado activo/inactivo.

        Returns:
            La instancia modificada o None si no se encontró
        """
        instance = self.get(id)
        if instance is None:
            return None

        if hasattr(instance, 'active'):
            instance.active = not instance.active
        elif hasattr(instance, 'is_active'):
            instance.is_active = not instance.is_active

        return self.repository.update(instance)

    def delete(self, id: int, delete_type: str = 'logical') -> Any:
        """
        Elimina un registro según el tipo especificado.

        Args:
            id: ID del registro
            delete_type: 'logical', 'persistential' o 'physical'

        Returns:
            Dependiendo del tipo:
            - logical/persistential: La instancia modificada
            - physical: bool (resultado de la eliminación)
        """
        if delete_type == 'physical':
            return super().delete(id)
        elif delete_type == 'persistential':
            return self.persistential_delete(id)
        elif delete_type == 'logical':
            return self.logical_delete(id)
        else:
            raise ValueError("delete_type debe ser 'logical', 'persistential' o 'physical'")
