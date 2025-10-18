from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.AsignationInstructorService import AsignationInstructorService
from apps.assign.entity.serializers.AsignationInstructor.AsignationInstructorSerializer import AsignationInstructorSerializer



class AsignationInstructorViewset(BaseViewSet):
    """
    ViewSet for managing instructor assignments.
    All internal code, comments, and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """
    service_class = AsignationInstructorService
    serializer_class = AsignationInstructorSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las asignaciones de instructor.",
        tags=["AsignationInstructor"]
    )
    def list(self, request, *args, **kwargs):
        """Return a list of all instructor assignments."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva asignación de instructor.",
        tags=["AsignationInstructor"]
    )
    def create(self, request, *args, **kwargs):
        """Create a new instructor assignment."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de una asignación específica.",
        tags=["AsignationInstructor"]
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve information for a specific instructor assignment."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una asignación.",
        tags=["AsignationInstructor"]
    )
    def update(self, request, *args, **kwargs):
        """Update all information for an instructor assignment."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una asignación.",
        tags=["AsignationInstructor"]
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update fields of an instructor assignment."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente una asignación de la base de datos.",
        tags=["AsignationInstructor"]
    )
    def destroy(self, request, *args, **kwargs):
        """Physically delete an instructor assignment from the database."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) de la asignación especificada.",
        tags=["AsignationInstructor"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete of the specified instructor assignment.
        """
        return super().soft_destroy(request, pk)
