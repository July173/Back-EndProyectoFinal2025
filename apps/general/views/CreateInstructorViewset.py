from apps.general.entity.serializers.CreateInstructorSerializer import CreateInstructorFlatSerializer
from apps.general.services.InstructorService import InstructorService
from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction


class CreateInstructorViewset(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=CreateInstructorFlatSerializer,
        operation_description="Crea un nuevo instructor con todos los campos al mismo nivel.",
        tags=["Instructor"]
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateInstructorFlatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Separar los datos
        person_data = {k: data[k] for k in [
            'first_name', 'second_name', 'first_last_name', 'second_last_name',
            'phone_number', 'type_identification', 'number_identification'
        ]}
        user_data = {k: data[k] for k in ['email', 'password', 'role_id']}
        instructor_data = {k: data[k] for k in [
            'contractType', 'contractStartDate', 'contractEndDate', 'knowledgeArea'
        ]}

        service = InstructorService()
        try:
            with transaction.atomic():
                result = service.create_instructor(person_data, user_data, instructor_data)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
