from abc import ABC, abstractmethod
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any


class IBaseViewSet(ABC):
    """Interfaz para ViewSets personalizados."""

    @abstractmethod
    def list(self, request: Request) -> Response:
        pass

    @abstractmethod
    def retrieve(self, request: Request, pk: Any = None) -> Response:
        pass

    @abstractmethod
    def create(self, request: Request) -> Response:
        pass

    @abstractmethod
    def update(self, request: Request, pk: Any = None) -> Response:
        pass

    @abstractmethod
    def partial_update(self, request: Request, pk: Any = None) -> Response:
        pass

    @abstractmethod
    def destroy(self, request: Request, pk: Any = None) -> Response:
        pass
