from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.UserService import UserService
from apps.security.entity.serializers.UserSerializer import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(BaseViewSet):

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
        Restablece la contraseña usando email, código y nueva contraseña.
        """
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        result = self.service.reset_password(email, new_password)
        return Response(result['data'], status=result['status'])
    service_class = UserService
    serializer_class = UserSerializer


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
        Valida correo institucional y contraseña, retorna JWT si es válido.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        result = self.service.validate_institutional_login(email, password)
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
        Solicita código de recuperación de contraseña, lo envía por email y lo retorna al frontend.
        """
        email = request.data.get('email')
        result = self.service.send_password_reset_code(email)
        return Response(result['data'], status=result['status'])
    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los usuarios registrados."
        ),
        tags=["User"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo usuario con la información proporcionada."
        ),
        tags=["User"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un usuario específico."
        ),
        tags=["User"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un usuario."
        ),
        tags=["User"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un usuario."
        ),
        tags=["User"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un usuario de la base de datos."
        ),
        tags=["User"]
    )
    def destroy(self, request, *args, **kwargs):
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

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los usuarios registrados."
        ),
        tags=["User"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo usuario con la información proporcionada."
        ),
        tags=["User"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un usuario específico."
        ),
        tags=["User"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un usuario."
        ),
        tags=["User"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un usuario."
        ),
        tags=["User"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un usuario de la base de datos."
        ),
        tags=["User"]
    )
    def destroy(self, request, *args, **kwargs):
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
