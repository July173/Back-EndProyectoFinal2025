from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.UserService import UserService
from apps.security.entity.serializers.UserSerializer import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(BaseViewSet):

    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        """
        Restablece la contraseña usando email, código y nueva contraseña.
        """
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        result = self.service.reset_password(email, code, new_password)
        return Response(result['data'], status=result['status'])
    service_class = UserService
    serializer_class = UserSerializer


    @action(detail=False, methods=['post'], url_path='validate-institutional-login')
    def validate_institutional_login(self, request):
        """
        Valida correo institucional y contraseña, retorna JWT si es válido.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        result = self.service.validate_institutional_login(email, password)
        return Response(result['data'], status=result['status'])

    @action(detail=False, methods=['post'], url_path='request-password-reset')
    def request_password_reset(self, request):
        """
        Solicita código de recuperación de contraseña, lo envía por email y lo retorna al frontend.
        """
        email = request.data.get('email')
        result = self.service.send_password_reset_code(email)
        return Response(result['data'], status=result['status'])
