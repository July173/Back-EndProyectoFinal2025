from typing import TypeVar, Dict, Any
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

    def soft_delete(self, id: int) -> bool:
        return super().soft_delete(id)
