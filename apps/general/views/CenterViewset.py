from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.CenterService import CenterService
from apps.general.entity.serializers.CenterSerializer import CenterSerializer


class CenterViewset(BaseViewSet):
    """
    ViewSet for managing Center CRUD operations and custom endpoints.
    All internal comments and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """

    service_class = CenterService
    serializer_class = CenterSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los centros registrados.",
        tags=["Center"]
    )
    def list(self, request, *args, **kwargs):
        """
        List all centers.
        """
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo centro con la información proporcionada.",
        tags=["Center"]
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new center with the provided information.
        """
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un centro específico.",
        tags=["Center"]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve information for a specific center.
        """
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un centro.",
        tags=["Center"]
    )
    def update(self, request, *args, **kwargs):
        """
        Update all information for a center.
        """
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un centro.",
        tags=["Center"]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update fields for a center.
        """
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un centro de la base de datos.",
        tags=["Center"]
    )
    def destroy(self, request, *args, **kwargs):
        """
        Physically delete a center from the database.
        """
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del centro especificado.",
        tags=["Center"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete for the specified center.
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
        