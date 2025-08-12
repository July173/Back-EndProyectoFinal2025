from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from typing import Type, Any
from core.base.view.interfaces.IBaseViewset import IBaseViewSet
from core.base.services.interfaces.IBaseService import IBaseService
from rest_framework.serializers import Serializer


class BaseViewSet(viewsets.ViewSet, IBaseViewSet):
    """
    Implementación concreta del ViewSet que sigue nuestra arquitectura.
    """
    service_class: Type[IBaseService] = None
    serializer_class: Type[Serializer] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_dependencies()
        self.service = self.service_class()

    def _validate_dependencies(self):
        if not self.service_class:
            raise NotImplementedError("Debe definir 'service_class'")
        if not self.serializer_class:
            raise NotImplementedError("Debe definir 'serializer_class'")

    def get_serializer_class(self) -> Type[Serializer]:
        return self.serializer_class

    def get_serializer(self, *args, **kwargs) -> Serializer:
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def list(self, request: Request) -> Response:
        items = self.service.list()
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: Any = None) -> Response:
        item = self.service.get(pk)
        if not item:
            return Response(
                {"detail": "No encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.service.create(serializer.validated_data)
        output_serializer = self.get_serializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: Any = None) -> Response:
        instance = self.service.get(pk)
        if not instance:
            return Response(
                {"detail": "No encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = self.service.update(pk, serializer.validated_data)
        output_serializer = self.get_serializer(updated_instance)
        return Response(output_serializer.data)

    def partial_update(self, request: Request, pk: Any = None) -> Response:
        if not request.data:  # Si el cuerpo está vacío
            instance = self.service.get(pk)
            if not instance:
                return Response(
                    {"detail": "No encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )
            response_serializer = self.get_serializer(instance)
            return Response(response_serializer.data)
        # Si hay datos, actualiza normalmente
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = self.service.partial_update(pk, serializer.validated_data)
        response_serializer = self.get_serializer(updated_instance)
        return Response(response_serializer.data)

    def destroy(self, request: Request, pk: Any = None) -> Response:
        deleted = self.service.delete(pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"detail": "No encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
