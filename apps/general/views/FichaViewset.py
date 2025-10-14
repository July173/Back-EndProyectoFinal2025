from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.FichaService import FichaService
from apps.general.entity.serializers.FichaSerializer import FichaSerializer


class FichaViewset(BaseViewSet):
    """
    ViewSet for managing Ficha CRUD operations and custom endpoints.
    All internal comments and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """

    service_class = FichaService
    serializer_class = FichaSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las fichas registradas.",
        tags=["Ficha"]
    )
    def list(self, request, *args, **kwargs):
        """
        List all fichas.
        """
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea una nueva ficha con la información proporcionada.",
        tags=["Ficha"]
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new ficha with the provided information.
        """
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de una ficha específica.",
        tags=["Ficha"]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve information for a specific ficha.
        """
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una ficha.",
        tags=["Ficha"]
    )
    def update(self, request, *args, **kwargs):
        """
        Update all information for a ficha.
        """
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una ficha.",
        tags=["Ficha"]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update fields for a ficha.
        """
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente una ficha de la base de datos.",
        tags=["Ficha"]
    )
    def destroy(self, request, *args, **kwargs):
        """
        Physically delete a ficha from the database.
        """
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) de la ficha especificada.",
        tags=["Ficha"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete for the specified ficha.
        """
        deleted = self.service_class().soft_delete(pk)
        if deleted:
            return Response(
                {"detail": "Eliminado lógicamente correctamente."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "No encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
