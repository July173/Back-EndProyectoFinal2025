from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.ModalityProductiveStageService import ModalityProductiveStageService
from apps.assign.entity.serializers.ModalityProductiveStageSerializer import ModalityProductiveStageSerializer



class ModalityProductiveStageViewset(BaseViewSet):
    """
    ViewSet for managing productive stage modality entities.
    All internal code, comments, and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """
    service_class = ModalityProductiveStageService
    serializer_class = ModalityProductiveStageSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las modalidades de etapa productiva.",
        tags=["ModalityProductiveStage"]
    )
    def list(self, request, *args, **kwargs):
        """Return a list of all registered productive stage modalities."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva modalidad de etapa productiva.",
        tags=["ModalityProductiveStage"]
    )
    def create(self, request, *args, **kwargs):
        """Create a new productive stage modality with the provided information."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de una modalidad específica.",
        tags=["ModalityProductiveStage"]
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve information for a specific productive stage modality."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una modalidad.",
        tags=["ModalityProductiveStage"]
    )
    def update(self, request, *args, **kwargs):
        """Update all information for a productive stage modality."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una modalidad.",
        tags=["ModalityProductiveStage"]
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update fields of a productive stage modality."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente una modalidad de la base de datos.",
        tags=["ModalityProductiveStage"]
    )
    def destroy(self, request, *args, **kwargs):
        """Physically delete a productive stage modality from the database."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) de la modalidad especificada.",
        tags=["ModalityProductiveStage"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete of the specified productive stage modality.
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
