from apps.general.entity.models import Instructor
from apps.general.entity.serializers.CreateInstructor.CreateInstructorSerializer import CreateInstructorSerializer
from apps.general.entity.serializers.CreateInstructor.GetInstructorSerializer import GetInstructorSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from apps.general.services.CreateInstructorService import CreateInstructorService
from rest_framework.decorators import action


class CreateInstructorViewset(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="Obtiene un instructor por su ID.",
        responses={200: GetInstructorSerializer},
        tags=["Instructor"]
    )
    def retrieve(self, request, pk=None):
        instructor = self.service.get_instructor(pk)
        if instructor:
            serializer = GetInstructorSerializer(instructor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    service = CreateInstructorService()

    @swagger_auto_schema(
        request_body=CreateInstructorSerializer,
        operation_description="Crea un nuevo instructor.",
        tags=["Instructor"]
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = self.service.create_instructor(
            {k: data[k] for k in ['first_name', 'second_name', 'first_last_name', 'second_last_name', 'phone_number', 'type_identification', 'number_identification']},
            {k: data[k] for k in ['email', 'role_id', 'password'] if k in data},
            {k: data[k] for k in ['contractType', 'contractStartDate', 'contractEndDate', 'knowledgeArea']},
            data['sede_id'],
            data['center_id'],
            data['regional_id']
        )
        return Response({"detail": "Instructor creado correctamente.", "ids": result}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Lista todos los instructores.",
        responses={200: GetInstructorSerializer(many=True)},
        tags=["Instructor"]
    )
    def list(self, request, *args, **kwargs):
        instructors = self.service.list_instructors()
        serializer = GetInstructorSerializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CreateInstructorSerializer,
        operation_description="Actualiza un instructor existente.",
        tags=["Instructor"]
    )
    def update(self, request, pk=None):
        serializer = CreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = self.service.update_instructor(
                pk,
                {k: data[k] for k in ['first_name', 'second_name', 'first_last_name', 'second_last_name', 'phone_number', 'type_identification', 'number_identification']},
                {k: data[k] for k in ['email', 'role_id'] if k in data},
                {k: data[k] for k in ['contractType', 'contractStartDate', 'contractEndDate', 'knowledgeArea'] if k in data},
                data.get('sede_id')
            )
            return Response({"detail": "Instructor actualizado correctamente.", "ids": result}, status=status.HTTP_200_OK)
        except Instructor.DoesNotExist:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Elimina un instructor (delete persistencial).",
        tags=["Instructor"]
    )
    def destroy(self, request, pk=None):
        try:
            self.service.delete_instructor(pk)
            return Response({"detail": "Instructor eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Instructor.DoesNotExist:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Elimina lógicamente o reactiva un instructor y sus relaciones.",
        tags=["Instructor"]
    )
    @action(detail=True, methods=['delete'], url_path='logical-delete')
    def logical_delete(self, request, pk=None):
        try:
            result = self.service.logical_delete_instructor(pk)
            return Response({"detail": result}, status=status.HTTP_200_OK)
        except Instructor.DoesNotExist:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
