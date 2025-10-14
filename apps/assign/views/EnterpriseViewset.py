from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.EnterpriseService import EnterpriseService
from apps.assign.entity.serializers.EnterpriseSerializer import EnterpriseSerializer



class EnterpriseViewset(BaseViewSet):
    """
    ViewSet for managing enterprise entities.
    All internal code, comments, and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """
    service_class = EnterpriseService
    serializer_class = EnterpriseSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las empresas registradas.",
        tags=["Enterprise"]
    )
    def list(self, request, *args, **kwargs):
        """Return a list of all registered enterprises."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva empresa con la información proporcionada.",
        tags=["Enterprise"]
    )
    def create(self, request, *args, **kwargs):
        """Create a new enterprise with the provided information."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de una empresa específica.",
        tags=["Enterprise"]
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve information for a specific enterprise."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una empresa.",
        tags=["Enterprise"]
    )
    def update(self, request, *args, **kwargs):
        """Update all information for an enterprise."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una empresa.",
        tags=["Enterprise"]
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update fields of an enterprise."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente una empresa de la base de datos.",
        tags=["Enterprise"]
    )
    def destroy(self, request, *args, **kwargs):
        """Physically delete an enterprise from the database."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) de la empresa especificada.",
        tags=["Enterprise"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete of the specified enterprise.
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
