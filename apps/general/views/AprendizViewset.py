from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.general.entity.models import Apprentice
from apps.general.entity.serializers.CreateAprendiz.CreateApprenticeSerializer import CreateApprenticeSerializer
from apps.general.entity.serializers.CreateAprendiz.GetApprenticeSerializer import GetApprenticeSerializer
from apps.general.entity.serializers.CreateAprendiz.UpdateApprenticeSerializer import UpdateApprenticeSerializer
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.AprendizService import ApprenticeService
from apps.general.entity.serializers.CreateAprendiz.ApprenticeSerializer import ApprenticeSerializer


class ApprenticeViewset(BaseViewSet):

    service_class = ApprenticeService
    serializer_class = ApprenticeSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los aprendices registrados.",
        tags=["Aprendiz"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo aprendiz con la información proporcionada.",
        tags=["Aprendiz"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un aprendiz específico.",
        tags=["Aprendiz"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un aprendiz.",
        tags=["Aprendiz"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un aprendiz.",
        tags=["Aprendiz"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un aprendiz de la base de datos.",
        tags=["Aprendiz"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del aprendiz especificado.",
        tags=["Aprendiz"],
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
#--------------------------------------------------------------------------------------------

    # ----------- RETRIEVE (custom) -----------
    @swagger_auto_schema(
        operation_description="Obtiene un aprendiz por su ID (nuevo endpoint avanzado).",
        responses={200: GetApprenticeSerializer},
        tags=["Aprendiz"]
    )
    @action(detail=True, methods=['get'], url_path='Create-Aprendiz/GetById')
    def custom_retrieve(self, request, pk=None):
        aprendiz = self.service.get_aprendiz(pk)
        if aprendiz:
            serializer = GetApprenticeSerializer(aprendiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Aprendiz no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # ----------- CREATE (custom) -----------
    @swagger_auto_schema(
        request_body=CreateApprenticeSerializer,
        operation_description="Crea un nuevo aprendiz (nuevo endpoint avanzado).",
        tags=["Aprendiz"]
    )
    @action(detail=False, methods=['post'], url_path='Create-Aprendiz/create')
    def custom_create(self, request, *args, **kwargs):
        serializer = CreateApprenticeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aprendiz, user, person = self.service.create_aprendiz(serializer.validated_data)
        return Response({
            "detail": "Aprendiz creado correctamente.",
            "id": aprendiz.id,
            "user_id": user.id,
            "person_id": person.id,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

    # ----------- LIST (custom) -----------
    @swagger_auto_schema(
        operation_description="Lista todos los aprendices (nuevo endpoint avanzado).",
        responses={200: GetApprenticeSerializer(many=True)},
        tags=["Aprendiz"]
    )
    @action(detail=False, methods=['get'], url_path='Create-Aprendiz/list')
    def custom_list(self, request, *args, **kwargs):
        aprendices = self.service.list_aprendices()
        serializer = GetApprenticeSerializer(aprendices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ----------- UPDATE (custom) -----------
    @swagger_auto_schema(
        request_body=UpdateApprenticeSerializer,
        operation_description="Actualiza los datos de un aprendiz (nuevo endpoint avanzado).",
        tags=["Aprendiz"]
    )
    @action(detail=True, methods=['put'], url_path='Create-Aprendiz/update')
    def custom_update(self, request, pk=None):
        serializer = UpdateApprenticeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            aprendiz = self.service.update_aprendiz(pk, serializer.validated_data)
            return Response({"detail": "Aprendiz actualizado correctamente.", "id": aprendiz.id}, status=status.HTTP_200_OK)
        except Apprentice.DoesNotExist:
            return Response({"detail": "Aprendiz no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ----------- DELETE (custom) -----------
    @swagger_auto_schema(
        operation_description="Elimina un aprendiz (delete persistencial, nuevo endpoint avanzado).",
        tags=["Aprendiz"]
    )
    @action(detail=True, methods=['delete'], url_path='Create-Aprendiz/delete')
    def custom_destroy(self, request, pk=None):
        try:
            self.service.delete_apprentice(pk)
            return Response({"detail": "Aprendiz eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Apprentice.DoesNotExist:
            return Response({"detail": "Aprendiz no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    # ----------- LOGICAL DELETE OR REACTIVATE -----------
    @swagger_auto_schema(
        operation_description="Elimina lógicamente o reactiva un aprendiz (nuevo endpoint avanzado).",
        tags=["Aprendiz"]
    )
    @action(detail=True, methods=['delete'], url_path='Create-Aprendiz/logical-delete')
    def custom_logical_delete(self, request, pk=None):
        try:
            result = self.service.logical_delete_apprentice(pk)
            return Response({"detail": result}, status=status.HTTP_200_OK)
        except Apprentice.DoesNotExist:
            return Response({"detail": "Aprendiz no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
