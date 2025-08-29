from apps.general.entity.models import Instructor, PersonSede, Sede
from apps.general.entity.models.KnowledgeArea import KnowledgeArea
from apps.security.entity.models import Person, User
from apps.general.entity.serializers.CreateInstructor.CreateInstructorSerializer import CreateInstructorSerializer
from apps.general.entity.serializers.CreateInstructor.GetInstructorSerializer import GetInstructorSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class CreateInstructorViewset(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=CreateInstructorSerializer,
        operation_description="Crea un nuevo instructor.",
        tags=["Instructor"]
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 1. Crear la persona
        person = Person.objects.create(
            first_name=data['first_name'],
            second_name=data.get('second_name', ''),
            first_last_name=data['first_last_name'],
            second_last_name=data.get('second_last_name', ''),
            phone_number=data.get('phone_number', ''),
            type_identification=data['type_identification'],
            number_identification=data['number_identification']
        )

        # 2. Asociar la persona con la sede
        sede_instance = Sede.objects.get(pk=data['sede_id'])
        PersonSede.objects.create(
            SedeId=sede_instance,
            PersonId=person
        )

        # 3. Crear el usuario
        User.objects.create(
            person=person,
            email=data['email'],
            role_id=3  # O el rol que corresponda
        )

        # 4. Crear el instructor
        knowledge_area_instance = KnowledgeArea.objects.get(pk=data['knowledgeArea'])
        Instructor.objects.create(
            person=person,
            contractType=data['contractType'],
            contractStartDate=data['contractStartDate'],
            contractEndDate=data['contractEndDate'],
            knowledgeArea=knowledge_area_instance,
            active=True
        )

        return Response({"detail": "Instructor creado correctamente."}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Lista todos los instructores.",
        responses={200: GetInstructorSerializer(many=True)},
        tags=["Instructor"]
    )
    def list(self, request, *args, **kwargs):
        instructors = Instructor.objects.all()
        serializer = GetInstructorSerializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
