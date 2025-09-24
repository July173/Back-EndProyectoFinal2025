from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.AsignationInstructorService import AsignationInstructorService
from apps.assign.entity.serializers.AsignationInstructorSerializer import AsignationInstructorSerializer


class AsignationInstructorViewset(BaseViewSet):
    
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las asignaciones de instructor.",
        tags=["AsignationInstructor"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva asignación de instructor.",
        tags=["AsignationInstructor"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de una asignación específica.",
        tags=["AsignationInstructor"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una asignación.",
        tags=["AsignationInstructor"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una asignación.",
        tags=["AsignationInstructor"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente una asignación de la base de datos.",
        tags=["AsignationInstructor"]
    )
    def destroy(self, request, *args, **kwargs):
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



    @swagger_auto_schema(
        method='post',
        operation_description="Crea una asignación de instructor personalizada (fecha automática)",
        request_body=AsignationInstructorSerializer,
        responses={
            201: openapi.Response("Asignación creada correctamente", AsignationInstructorSerializer),
            400: "Datos inválidos"
        },
        tags=["AsignationInstructor"]
    )
    @action(detail=False, methods=['post'], url_path='custom-create')
    def custom_create(self, request):
        instructor_id = request.data.get('instructor')
        request_asignation_id = request.data.get('request_asignation')
        if not instructor_id or not request_asignation_id:
            return Response({"detail": "Faltan datos obligatorios."}, status=status.HTTP_400_BAD_REQUEST)
        service = self.service_class()
        asignation = service.create_custom(instructor_id, request_asignation_id)
        serializer = self.serializer_class(asignation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    service_class = AsignationInstructorService
    serializer_class = AsignationInstructorSerializer
