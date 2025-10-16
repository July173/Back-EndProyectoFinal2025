from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.PersonService import PersonService
from apps.security.entity.serializers.person.PatchPersonSerializer import PatchPersonSerializer
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.person.RegisterAprendizSerializer import RegisterAprendizSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



class PersonViewSet(BaseViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    service_class = PersonService
    serializer_class = PersonSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return PatchPersonSerializer
        elif self.action == 'register_apprentice':
            return RegisterAprendizSerializer
        return PersonSerializer

    #--- REGISTER APPRENTICE ---
    @swagger_auto_schema(
        operation_description=(
            "Registers a new apprentice in the system.\n\n"
            "• **Email**: Must be provided by the user (format: usuario@soy.sena.edu.co)\n"
            "• **Password**: Will be set when an administrator activates the account\n\n"
            "The apprentice is registered but inactive until an administrator activates the account."
        ),
        operation_summary="Apprentice registration with pending activation",
        tags=["Person - Registro"],
        request_body=RegisterAprendizSerializer,
        responses={
            201: openapi.Response(
                description="Registro exitoso, pendiente de activación",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'persona': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'first_last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'number_identification': openapi.Schema(type=openapi.TYPE_STRING),
                                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                                'type_identification': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de DocumentType"),
                                'email': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        ),
                        'usuario': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Correo proporcionado por el usuario"
                                ),
                                'is_active': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description="Siempre false inicialmente, requiere activación por administrador"
                                ),
                                'role': openapi.Schema(type=openapi.TYPE_INTEGER, description="Rol 2 = Aprendiz")
                            }
                        ),
                        'apprentice_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'success': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                ),
                examples={
                    'application/json': {
                        'persona': {
                            'id': 1,
                            'first_name': 'Juan',
                            'first_last_name': 'Pérez',
                            'number_identification': '1234567890',
                            'phone_number': '3001234567',
                            'type_identification': 1,
                            'email': 'juan.perez@soy.sena.edu.co'
                        },
                        'usuario': {
                            'id': 1,
                            'email': 'juan.perez@soy.sena.edu.co',
                            'is_active': False,
                            'role': 2
                        },
                        'apprentice_id': 1,
                        'success': 'Usuario registrado correctamente. Tu cuenta está pendiente de activación por un administrador.'
                    }
                }
            ),
            400: openapi.Response(
                description="Error en el registro",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Descripción del error"
                        ),
                        'detalle': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Detalles específicos del error"
                        )
                    }
                ),
                examples={
                    'application/json': {
                        'error': 'El correo institucional ya está registrado.'
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['post'], url_path='register-apprentice')
    def register_apprentice(self, request):
        """
        Controller: Only orchestrates the call to the service.
        Does not contain validations or business logic.
        """
        result = self.service.register_apprentice(request.data)
        return Response(result['data'], status=result['status'])

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Gets a list of all registered people."
        ),
        tags=["Person"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Creates a new person with the provided information."
        ),
        tags=["Person"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Gets the information of a specific person."
        ),
        tags=["Person"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Updates the complete information of a person."
        ),
        tags=["Person"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Updates only some fields of a person."
        ),
        tags=["Person"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Physically deletes a person from the database."
        ),
        tags=["Person"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Performs a logical (soft) delete of the specified person."
        ),
        tags=["Person"],
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
