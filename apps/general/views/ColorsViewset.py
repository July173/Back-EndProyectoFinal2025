from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.ColorsService import ColorsService
from apps.general.entity.serializers.ColorsSerializer import ColorsSerializer

class ColorsViewset(BaseViewSet):
    """
    ViewSet for Colors entity.
    """
    service_class = ColorsService
    serializer_class = ColorsSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los colores registrados.",  # User-facing description in Spanish
        tags=["Colors"]
    )
    def list(self, request, *args, **kwargs):
        """
        List all registered colors.
        """
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo color.",  # User-facing description in Spanish
        tags=["Colors"]
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new color.
        """
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un color específico.",  # User-facing description in Spanish
        tags=["Colors"]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve information for a specific color.
        """
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un color.",  # User-facing description in Spanish
        tags=["Colors"]
    )
    def update(self, request, *args, **kwargs):
        """
        Update all information for a color.
        """
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un color.",  # User-facing description in Spanish
        tags=["Colors"]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update fields of a color.
        """
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un color de la base de datos.",  # User-facing description in Spanish
        tags=["Colors"]
    )
    def destroy(self, request, *args, **kwargs):
        """
        Physically delete a color from the database.
        """
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del color especificado.",  # User-facing description in Spanish
        tags=["Colors"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),  # User-facing message in Spanish
            404: openapi.Response("No encontrado.")  # User-facing message in Spanish
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Perform a logical (soft) delete for the specified color.
        """
        return super().soft_destroy(request, pk)
   