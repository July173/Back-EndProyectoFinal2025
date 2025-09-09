from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from apps.general.entity.serializers.CreateAprendiz.CreateAprendizSerializer import CreateAprendizSerializer
from apps.general.services.CreateAprendizService import CreateAprendizService
from apps.general.entity.serializers.CreateAprendiz.GetAprendizSerializer import GetAprendizSerializer
from apps.general.entity.models import Aprendiz
from apps.general.entity.serializers.CreateAprendiz.UpdateAprendizSerializer import UpdateAprendizSerializer

class CreateAprendizViewset(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="Obtiene un aprendiz por su ID.",
        responses={200: GetAprendizSerializer},
        tags=["Aprendiz"]
    )
    def retrieve(self, request, pk=None):
        try:
            aprendiz = Aprendiz.objects.get(pk=pk)
            serializer = GetAprendizSerializer(aprendiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Aprendiz.DoesNotExist:
            return Response({"detail": "Aprendiz no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    service = CreateAprendizService()

    @swagger_auto_schema(
        request_body=CreateAprendizSerializer,
        operation_description="Crea un nuevo aprendiz.",
        tags=["Aprendiz"]
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateAprendizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        person_data = {
            'type_identification': data['type_identification'],
            'number_identification': data['number_identification'],
            'first_name': data['first_name'],
            'second_name': data.get('second_name', ''),
            'first_last_name': data['first_last_name'],
            'second_last_name': data.get('second_last_name', ''),
            'phone_number': data.get('phone_number', ''),
        }
        user_data = {
            'email': data['email'],
            'person_id': None  # Se asigna en el service
        }
        ficha_id = data['ficha_id']

        aprendiz = self.service.create_aprendiz(person_data, user_data, ficha_id)
        return Response({"detail": "Aprendiz creado correctamente.", "id": aprendiz.id}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Lista todos los aprendices.",
        responses={200: GetAprendizSerializer(many=True)},
        tags=["Aprendiz"]
    )
    def list(self, request, *args, **kwargs):
        aprendices = Aprendiz.objects.all()
        serializer = GetAprendizSerializer(aprendices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UpdateAprendizSerializer,
        operation_description="Actualiza los datos de un aprendiz.",
        tags=["Aprendiz"]
    )
    def update(self, request, pk=None):
        serializer = UpdateAprendizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        person_data = {
            'type_identification': data['type_identification'],
            'number_identification': data['number_identification'],
            'first_name': data['first_name'],
            'second_name': data.get('second_name', ''),
            'first_last_name': data['first_last_name'],
            'second_last_name': data.get('second_last_name', ''),
            'phone_number': data.get('phone_number', ''),
        }
        user_data = {
            'email': data['email'],
        }
        ficha_id = data['ficha_id']
        role_id = data['role_id']

        try:
            aprendiz = self.service.update_aprendiz(pk, person_data, user_data, ficha_id, role_id)
            return Response({"detail": "Aprendiz actualizado correctamente.", "id": aprendiz.id}, status=status.HTTP_200_OK)
        except Aprendiz.DoesNotExist:
            return Response({"detail": "Aprendiz no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Elimina un aprendiz (delete persistencial).",
        tags=["Aprendiz"]
    )
    def destroy(self, request, pk=None):
        try:
            self.service.delete_aprendiz(pk)
            return Response({"detail": "Aprendiz eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Aprendiz.DoesNotExist:
            return Response({"detail": "Aprendiz no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Elimina lógicamente o reactiva un aprendiz.",
        tags=["Aprendiz"]
    )
    @action(detail=True, methods=['delete'], url_path='logical-delete')
    def logical_delete(self, request, pk=None):
        try:
            result = self.service.logical_delete_aprendiz(pk)
            return Response({"detail": result}, status=status.HTTP_200_OK)
        except Aprendiz.DoesNotExist:
            return Response({"detail": "Aprendiz no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)