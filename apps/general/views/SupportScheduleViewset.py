from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.SupportScheduleService import SupportScheduleService
from apps.general.entity.serializers.SupportScheduleSerializer import SupportScheduleSerializer
from apps.general.entity.models.SupportSchedule import SupportSchedule

class SupportScheduleViewset(BaseViewSet):
    """
    Viewset para operaciones CRUD sobre SupportSchedule.
    """
    service_class = SupportScheduleService
    serializer_class = SupportScheduleSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los horarios de soporte registrados.",
        tags=["SupportSchedule"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo horario de soporte.",
        tags=["SupportSchedule"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un horario de soporte específico.",
        tags=["SupportSchedule"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un horario de soporte.",
        tags=["SupportSchedule"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un horario de soporte.",
        tags=["SupportSchedule"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un horario de soporte de la base de datos.",
        tags=["SupportSchedule"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        operation_description="Elimina lógicamente (soft delete) un horario de soporte, marcándolo como inactivo.",
        tags=["SupportSchedule"]
    )
    @action(detail=True, methods=["delete"], url_path="soft-delete")
    def soft_delete(self, request, pk=None):
        instance = self.service.get(pk)
        if not instance:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        self.service.soft_delete(pk)
        return Response({"detail": "Eliminado lógicamente correctamente."}, status=status.HTTP_200_OK)
