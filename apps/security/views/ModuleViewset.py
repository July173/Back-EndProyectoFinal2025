from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.ModuleService import ModuleService
from apps.security.entity.serializers.ModuleSerializer import ModuleSerializer



class ModuleViewSet(BaseViewSet):
    @swagger_auto_schema(
        operation_description="Filters modules by status and name search.",
        tags=["Module"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Module status (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search text (module name)", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de módulos filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_modules(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        if active is not None:
            active = active.lower() in ['true', '1', 'yes']
        service = self.service_class()
        try:
            modules = service.get_filtered_modules(active, search)
            serializer = self.get_serializer(modules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"detail": str(ve)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Error inesperado: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    service_class = ModuleService
    serializer_class = ModuleSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Gets a list of all registered modules."
        ),
        tags=["Module"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Creates a new module with the provided information."
        ),
        tags=["Module"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Gets the information of a specific module."
        ),
        tags=["Module"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Updates the complete information of a module."
        ),
        tags=["Module"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Updates only some fields of a module."
        ),
        tags=["Module"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Physically deletes a module from the database."
        ),
        tags=["Module"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Performs a logical (soft) delete of the specified module."
        ),
        tags=["Module"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        try:
            deleted = self.service_class().soft_delete(pk)
            if deleted:
                return Response({"detail": "Eliminado lógicamente correctamente."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as ve:
            return Response({"detail": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Error inesperado: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
