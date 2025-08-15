from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.ProgramService import ProgramService
from apps.general.entity.serializers.ProgramSerializer import ProgramSerializer


class ProgramViewset(BaseViewSet):
    service_class = ProgramService
    serializer_class = ProgramSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los programas registrados."
        ),
        tags=["Programas"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo programa con la información proporcionada."
        ),
        tags=["Programas"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un programa específico."
        ),
        tags=["Programas"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un programa."
        ),
        tags=["Programas"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un programa."
        ),
        tags=["Programas"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un programa de la base de datos."
        ),
        tags=["Programas"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del programa especificado."
        ),
        tags=["Programas"],
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
