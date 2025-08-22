from apps.general.entity.serializers.CreateInstructorSerializer import CreateInstructorSerializer
from apps.general.services.CreateInstructorService import CreateInstructorService
from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction


class CreateInstructorViewset(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=CreateInstructorSerializer,
        operation_description="Crea un nuevo instructor con todos los campos al mismo nivel.",
        tags=["Instructor"]
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Separar los datos
        person_data = {k: data[k] for k in [
            'first_name', 'second_name', 'first_last_name', 'second_last_name',
            'phone_number', 'type_identification', 'number_identification'
        ]}
        # Asignar password y rol por defecto
        user_data = {
            'email': data['email'],
            'password': data['number_identification'],
            'role_id': 3
        }
        instructor_data = {k: data[k] for k in [
            'contractType', 'contractStartDate', 'contractEndDate', 'knowledgeArea'
        ]}
        # Extraer los IDs de relación
        sede_id = data['sede_id']
        center_id = data['center_id']
        regional_id = data['regional_id']

        service = CreateInstructorService()
        try:
            result = service.create_instructor(
                person_data, user_data, instructor_data, sede_id, center_id, regional_id
            )
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
