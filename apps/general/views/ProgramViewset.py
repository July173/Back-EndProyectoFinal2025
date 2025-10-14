from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.ProgramService import ProgramService
from apps.general.entity.serializers.ProgramSerializer import ProgramSerializer
from apps.general.entity.serializers.FichaSerializer import FichaSerializer

class ProgramViewset(BaseViewSet):
    """
    ViewSet for managing Program CRUD operations and custom endpoints.
    All internal comments and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """

    service_class = ProgramService
    serializer_class = ProgramSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los programas registrados."
        ),
        tags=["Program"]
    )
    def list(self, request, *args, **kwargs):
        """
        List all programs.
        """
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo programa con la información proporcionada."
        ),
        tags=["Program"]
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new program with the provided information.
        """
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un programa específico."
        ),
        tags=["Program"]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve information for a specific program.
        """
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un programa."
        ),
        tags=["Program"]
    )
    def update(self, request, *args, **kwargs):
        """
        Update all information for a program.
        """
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un programa."
        ),
        tags=["Program"]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update fields for a program.
        """
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un programa de la base de datos."
        ),
        tags=["Program"]
    )
    def destroy(self, request, *args, **kwargs):
        """
        Physically delete a program from the database.
        """
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del programa especificado."
        ),
        tags=["Program"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete for the specified program.
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

    # ----------- GET FICHAS BY PROGRAM (custom) -----------
    @swagger_auto_schema(
        operation_description="Obtiene todas las fichas vinculadas a un programa específico.",
        responses={200: FichaSerializer(many=True)},
        tags=["Program"]
    )
    @action(detail=True, methods=['get'], url_path='fichas')
    def get_fichas_by_program(self, request, pk=None):
        """
        Get all records (fichas) linked to a specific program.
        """
        fichas = self.service_class().get_fichas_by_program(pk)
        serializer = FichaSerializer(fichas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ----------- DISABLE PROGRAM WITH FICHAS (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description="Deshabilita o reactiva un programa y todas sus fichas vinculadas.",
        tags=["Program"],
        responses={
            200: "Acción realizada correctamente",
            400: "Error de validación", 
            404: "Programa no encontrado"
        }
    )
    @action(detail=True, methods=['delete'], url_path='disable-with-fichas')
    def disable_program_with_fichas(self, request, pk=None):
        """
        Disable or reactivate a program and all its linked records (fichas).
        """
        try:
            mensaje = self.service_class().logical_delete_program(pk)
            return Response(
                {"detail": mensaje},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
