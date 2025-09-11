from typing import TypeVar, List, Optional, Dict, Any
from core.base.repositories.interfaces.IBaseRepository import IBaseRepository

T = TypeVar("T")

class BaseService:
    """
    Implementación concreta del servicio con funcionalidades extendidas.

    Métodos principales:
    - list: Obtiene todos los registros del modelo.
    - get: Obtiene un registro por su ID.
    - create: Crea un nuevo registro con los datos dados.
    - update: Actualiza todos los campos de una instancia existente (PUT).
    - partial_update: Actualiza parcialmente los campos de una instancia existente (PATCH).
    - delete: Elimina físicamente un registro por ID.
    - soft_delete: Realiza borrado lógico (cambia active y delete_at).
    """

    def __init__(self, repository: IBaseRepository[T]):
        self.repository = repository

    def list(self) -> List[T]:
        """Obtiene todos los registros del modelo."""
        return self.repository.get_all()

    def get(self, id: int) -> Optional[T]:
        """Obtiene un registro por su ID."""
        return self.repository.get_by_id(id)

    def create(self, data: Dict[str, Any]) -> T:
        """Crea una nueva instancia a partir de los datos."""
        return self.repository.create(data)

    def update(self, id: int, data: Dict[str, Any]) -> T:
        """Actualiza todos los campos de una instancia existente (PUT)."""
        instance = self.get(id)
        if instance is None:
            raise ValueError(f"Instancia con id {id} no encontrada")
        for key, value in data.items():
            if value in [None, ""]:
                raise ValueError(f"El campo '{key}' no puede estar vacío")
            setattr(instance, key, value)
        return self.repository.update(instance)

    def partial_update(self, id: int, data: Dict[str, Any]) -> T:
        """Actualiza parcialmente los campos de una instancia existente (PATCH)."""
        instance = self.get(id)
        if instance is None:
            raise ValueError(f"Instancia con id {id} no encontrada")
        for key, value in data.items():
            if value not in [None, ""]:
                setattr(instance, key, value)
        return self.repository.update(instance)

    def delete(self, id: int) -> bool:
        """Elimina físicamente un registro por ID."""
        return self.repository.delete(id)

    def soft_delete(self, id: int) -> bool:
        """Realiza borrado lógico (cambia active y delete_at)."""
        return self.repository.soft_delete(id)
