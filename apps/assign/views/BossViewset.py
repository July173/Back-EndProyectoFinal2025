from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.BossService import BossService
from apps.assign.entity.serializers.BossSerializer import BossSerializer



class BossViewset(BaseViewSet):
    """
    ViewSet for managing boss entities.
    All internal code, comments, and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """
    service_class = BossService
    serializer_class = BossSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los jefes registrados.",
        tags=["Boss"]
    )
    def list(self, request, *args, **kwargs):
        """Return a list of all registered bosses."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo jefe con la información proporcionada.",
        tags=["Boss"]
    )
    def create(self, request, *args, **kwargs):
        """Create a new boss with the provided information."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de un jefe específico.",
        tags=["Boss"]
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve information for a specific boss."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un jefe.",
        tags=["Boss"]
    )
    def update(self, request, *args, **kwargs):
        """Update all information for a boss."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un jefe.",
        tags=["Boss"]
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update fields of a boss."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente un jefe de la base de datos.",
        tags=["Boss"]
    )
    def destroy(self, request, *args, **kwargs):
        """Physically delete a boss from the database."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del jefe especificado.",
        tags=["Boss"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete of the specified boss.
        User-facing messages remain in Spanish.
        """
        deleted = self.service_class().soft_delete(pk)
        if deleted:
            # Success message in Spanish for user-facing response
            return Response(
                {"detail": "Eliminado lógicamente correctamente."},
                status=status.HTTP_204_NO_CONTENT
            )
        # Error message in Spanish for user-facing response
        return Response(
            {"detail": "No encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
