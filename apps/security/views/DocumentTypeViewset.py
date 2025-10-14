from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.DocumentTypeService import DocumentTypeService
from apps.security.entity.serializers.DocumentTypeSerializer import DocumentTypeSerializer


class DocumentTypeViewset(BaseViewSet):
    service_class = DocumentTypeService
    serializer_class = DocumentTypeSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los tipos de documento registrados.",  # User-facing description in Spanish
        tags=["DocumentType"]
    )
    def list(self, request, *args, **kwargs):
        """
        List all registered document types.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo tipo de documento.",  # User-facing description in Spanish
        tags=["DocumentType"]
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new document type.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de un tipo de documento específico.",  # User-facing description in Spanish
        tags=["DocumentType"]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve information for a specific document type.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un tipo de documento.",  # User-facing description in Spanish
        tags=["DocumentType"]
    )
    def update(self, request, *args, **kwargs):
        """
        Update all information for a document type.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un tipo de documento.",  # User-facing description in Spanish
        tags=["DocumentType"]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update fields of a document type.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente un tipo de documento de la base de datos.",  # User-facing description in Spanish
        tags=["DocumentType"]
    )
    def destroy(self, request, *args, **kwargs):
        """
        Physically delete a document type from the database.
        """
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del tipo de documento especificado.",  # User-facing description in Spanish
        tags=["DocumentType"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),  # User-facing message in Spanish
            404: openapi.Response("No encontrado.")  # User-facing message in Spanish
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, pk=None):
        """
        Perform a logical (soft) delete for the specified document type.
        """
        deleted = self.service_class().soft_delete(pk)
        if deleted:
            return Response(
                {"detail": "Eliminado lógicamente correctamente."},  # User-facing message in Spanish
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "No encontrado."},  # User-facing message in Spanish
            status=status.HTTP_404_NOT_FOUND
        )
