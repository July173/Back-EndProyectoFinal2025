from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.UserService import UserService
from apps.security.entity.serializers.User.UserSerializer import UserSerializer
from apps.security.entity.serializers.User.UserSimpleSerializer import UserSimpleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(BaseViewSet):

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the current action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return UserSimpleSerializer
        return UserSerializer


    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los usuarios registrados."
        ),
        tags=["User"]
    )
    def list(self, request, *args, **kwargs):
        """
        Returns a list of all registered users.
        """
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo usuario con la información proporcionada."
        ),
        tags=["User"]
    )
    def create(self, request, *args, **kwargs):
        """
        Creates a new user with the provided information.
        """
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un usuario específico."
        ),
        tags=["User"]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves information for a specific user.
        """
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un usuario."
        ),
        tags=["User"]
    )
    def update(self, request, *args, **kwargs):
        """
        Updates all information for a user.
        """
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un usuario."
        ),
        tags=["User"]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates user fields.
        """
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un usuario de la base de datos."
        ),
        tags=["User"]
    )
    def destroy(self, request, *args, **kwargs):
        """
        Physically deletes a user from the database.
        """
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del usuario especificado."
        ),
        tags=["User"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Performs a logical (soft) delete of the specified user.
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

    @swagger_auto_schema(
        operation_description=(
            "Restablece la contraseña usando email y nueva contraseña."
        ),
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Correo institucional'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='Nueva contraseña'),
            },
            required=['email', 'new_password']
        ),
        responses={
            200: openapi.Response("Contraseña restablecida"),
            400: openapi.Response("Datos inválidos")
        }
    )
    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        """
        Resets the password using email and new password.
        """
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        result = self.service.reset_password(email, new_password)
        return Response(result['data'], status=result['status'])
    


    @swagger_auto_schema(
        operation_description=(
            "Valida correo institucional y contraseña, retorna JWT si es válido."
        ),
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Correo institucional'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña'),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response("Login exitoso"),
            400: openapi.Response("Datos inválidos")
        }
    )
    @action(detail=False, methods=['post'], url_path='validate-institutional-login')
    def validate_institutional_login(self, request):
        """
        Validates institutional email and password, returns JWT if valid.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        result = self.service.validate_institutional_login(email, password)
        print("user info: ", result['data'])
        print("user 2 info: ", result)
        return Response(result['data'], status=result['status'])

    @swagger_auto_schema(
        operation_description=(
            "Solicita código de recuperación de contraseña, lo envía por email y lo retorna al frontend."
        ),
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Correo institucional'),
            },
            required=['email']
        ),
        responses={
            200: openapi.Response("Código enviado"),
            400: openapi.Response("Datos inválidos")
        }
    )
    @action(detail=False, methods=['post'], url_path='request-password-reset')
    def request_password_reset(self, request):
        """
        Requests a password recovery code, sends it by email, and returns it to the frontend.
        """
        email = request.data.get('email')
        result = self.service.send_password_reset_code(email)
        return Response(result['data'], status=result['status'])
    

    @swagger_auto_schema(
        operation_description="Filtra usuarios por rol y búsqueda en nombre o documento.",
        tags=["User"],
        manual_parameters=[
            openapi.Parameter('role', openapi.IN_QUERY, description="Nombre del rol", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Texto de búsqueda (nombre o documento)", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de usuarios filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_users(self, request):
        """
        Filters users by role and search text (name or document).
        """
        role = request.query_params.get('role')
        search = request.query_params.get('search')
        service = self.service_class()
        users = service.get_filtered_users(role, search)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    service_class = UserService
    serializer_class = UserSerializer
