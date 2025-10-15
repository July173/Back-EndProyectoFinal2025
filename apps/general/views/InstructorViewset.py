from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.InstructorService import InstructorService
from apps.general.entity.serializers.CreateInstructor.InstructorSerializer import InstructorSerializer
from apps.general.entity.models import Instructor
from apps.general.entity.serializers.CreateInstructor.CreateInstructorSerializer import CreateInstructorSerializer
from apps.general.entity.serializers.CreateInstructor.GetInstructorSerializer import GetInstructorSerializer


class InstructorViewset(BaseViewSet):
    """
    ViewSet for managing Instructor CRUD operations and custom endpoints.
    All internal comments and docstrings are in English. User-facing messages and API documentation remain in Spanish.
    """

    service_class = InstructorService
    serializer_class = GetInstructorSerializer

    @swagger_auto_schema(
        operation_description="Filtra instructores por nombre, número de documento y área de conocimiento.",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Buscar por nombre o número de documento", type=openapi.TYPE_STRING),
            openapi.Parameter('knowledge_area_id', openapi.IN_QUERY, description="Filtrar por área de conocimiento (ID)", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response("Lista de instructores filtrados")},
        tags=["Instructor"]
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_instructors(self, request):
        """
        Filter instructors by name, document number, and knowledge area.
        """
        search = request.query_params.get('search')
        knowledge_area_id = request.query_params.get('knowledge_area_id')
        if knowledge_area_id:
            try:
                knowledge_area_id = int(knowledge_area_id)
            except ValueError:
                return Response({"detail": "El ID de área de conocimiento debe ser un número."}, status=status.HTTP_400_BAD_REQUEST)
        instructors = self.service_class().repository.get_filtered_instructors(search, knowledge_area_id)
        serializer = self.get_serializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        """
        Return all Instructor objects.
        """
        from apps.general.entity.models import Instructor
        return Instructor.objects.all()

    @swagger_auto_schema(
        method='patch',
        operation_description="Actualiza solo los campos assigned_learners y max_assigned_learners de un instructor.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'assigned_learners': openapi.Schema(type=openapi.TYPE_INTEGER, description='Aprendices actualmente asignados', nullable=True),
                'max_assigned_learners': openapi.Schema(type=openapi.TYPE_INTEGER, description='Límite máximo permitido', nullable=True)
            },
            required=[]
        ),
        responses={200: InstructorSerializer},
        tags=["Instructor"]
    )
    @action(detail=True, methods=['patch'], url_path='update-learners')
    def update_learners(self, request, pk=None):
        """
        Update only the assigned_learners and max_assigned_learners fields of an instructor.
        """
        service = InstructorService()
        assigned_learners = request.data.get('assigned_learners', None)
        max_assigned_learners = request.data.get('max_assigned_learners', None)
        try:
            instructor = service.update_learners_fields(pk, assigned_learners, max_assigned_learners)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if not instructor:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los instructores registrados.",
        manual_parameters=[
            openapi.Parameter(
                'is_followup_instructor',
                openapi.IN_QUERY,
                description="Filtrar instructores: 'all' (todos), 'true' (solo seguimiento), 'false' (solo no seguimiento)",
                type=openapi.TYPE_STRING,
                enum=['all', 'true', 'false']
            )
        ],
        tags=["Instructor"]
    )
    def list(self, request, *args, **kwargs):
        """
        List all instructors, with optional filtering by follow-up status.
        """
        is_followup = request.query_params.get('is_followup_instructor', 'all')
        queryset = self.get_queryset()
        if is_followup == 'true':
            queryset = queryset.filter(is_followup_instructor=True)
        elif is_followup == 'false':
            queryset = queryset.filter(is_followup_instructor=False)
        # If 'all', do not filter
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo instructor con la información proporcionada."
        ),
        tags=["Instructor"]
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new instructor with the provided information.
        """
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un instructor específico."
        ),
        tags=["Instructor"]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve information for a specific instructor.
        """
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un instructor."
        ),
        tags=["Instructor"]
    )
    def update(self, request, *args, **kwargs):
        """
        Update all information for an instructor.
        """
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un instructor."
        ),
        tags=["Instructor"]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update fields for an instructor.
        """
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un instructor de la base de datos."
        ),
        tags=["Instructor"]
    )
    def destroy(self, request, *args, **kwargs):
        """
        Physically delete an instructor from the database.
        """
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del instructor especificado."
        ),
        tags=["Instructor"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, pk=None):
        """
        Perform a logical (soft) delete for the specified instructor.
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

    # ----------- CUSTOM ENDPOINTS -----------

    @swagger_auto_schema(
        operation_description="Obtiene un instructor por su ID (nuevo endpoint avanzado).",
        responses={200: GetInstructorSerializer},
        tags=["Instructor"]
    )
    @action(detail=True, methods=['get'], url_path='Create-Instructor/Retrieve')
    def custom_retrieve(self, pk=None):
        """
        Retrieve an instructor by ID (advanced endpoint).
        """
        instructor = self.service.get_instructor(pk)
        if instructor:
            serializer = GetInstructorSerializer(instructor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    service = InstructorService()

    @swagger_auto_schema(
        request_body=CreateInstructorSerializer,
        operation_description="Crea un nuevo instructor (nuevo endpoint avanzado).",
        tags=["Instructor"]
    )
    @action(detail=False, methods=['post'], url_path='Create-Instructor/create')
    def custom_create(self, request, *args, **kwargs):
        """
        Create a new instructor (advanced endpoint).
        """
        serializer = CreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = self.service.create_instructor(
                {k: data[k] for k in ['first_name', 'second_name', 'first_last_name', 'second_last_name', 'phone_number', 'type_identification', 'number_identification']},
                {k: data[k] for k in ['email', 'role_id', 'password'] if k in data},
                {k: data[k] for k in ['contract_type', 'contract_start_date', 'contract_end_date', 'knowledge_area', 'is_followup_instructor'] if k in data},
                data['sede_id']
            )
            return Response({"detail": "Instructor creado correctamente.", "instructor_id": result["instructor_id"]}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            msg = str(e)
            if 'identificación' in msg:
                return Response({"detail": "Por favor selecciona un tipo de identificación válido."}, status=status.HTTP_400_BAD_REQUEST)
            elif 'contrato' in msg:
                return Response({"detail": "Por favor selecciona un tipo de contrato válido."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Lista todos los instructores (nuevo endpoint avanzado).",
        responses={200: GetInstructorSerializer(many=True)},
        tags=["Instructor"]
    )
    @action(detail=False, methods=['get'], url_path='custom-list')
    def custom_list(self):
        """
        List all instructors (advanced endpoint).
        """
        instructors = self.service.list_instructors()
        serializer = GetInstructorSerializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CreateInstructorSerializer,
        operation_description="Actualiza un instructor existente (nuevo endpoint avanzado).",
        tags=["Instructor"]
    )
    @action(detail=True, methods=['put'], url_path='Create-Instructor/update')
    def custom_update(self, request, pk=None):
        """
        Update an existing instructor (advanced endpoint).
        """
        serializer = CreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = self.service.update_instructor(
                pk,
                {k: data[k] for k in ['first_name', 'second_name', 'first_last_name', 'second_last_name', 'phone_number', 'type_identification', 'number_identification']},
                {k: data[k] for k in ['email', 'role_id'] if k in data},
                {k: data[k] for k in ['contractType', 'contractStartDate', 'contractEndDate', 'knowledgeArea', 'is_followup_instructor'] if k in data},
                data.get('sede_id')
            )
            return Response({"detail": "Instructor actualizado correctamente.", "ids": result}, status=status.HTTP_200_OK)
        except Instructor.DoesNotExist:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            msg = str(e)
            if 'identificación' in msg:
                return Response({"type_identification": [msg]}, status=status.HTTP_400_BAD_REQUEST)
            elif 'contrato' in msg:
                return Response({"contract_type": [msg]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Elimina un instructor (delete persistencial, nuevo endpoint avanzado).",
        tags=["Instructor"]
    )
    @action(detail=True, methods=['delete'], url_path='Create-Instructor/destroy')
    def custom_destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete an instructor (persistent delete, advanced endpoint).
        """
        try:
            self.service.delete_instructor(pk)
            return Response({"detail": "Instructor eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Instructor.DoesNotExist:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Elimina lógicamente o reactiva un instructor y sus relaciones (nuevo endpoint avanzado).",
        tags=["Instructor"]
    )
    @action(detail=True, methods=['delete'], url_path='Create-Instructor/logical-delete')
    def custom_logical_delete(self, request, pk=None):
        """
        Logically delete or reactivate an instructor and its relations (advanced endpoint).
        """
        try:
            result = self.service.logical_delete_instructor(pk)
            return Response({"detail": result}, status=status.HTTP_200_OK)
        except Instructor.DoesNotExist:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


