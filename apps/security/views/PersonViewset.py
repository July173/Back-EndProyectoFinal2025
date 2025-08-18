from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.PersonService import PersonService
from apps.security.entity.serializers.PersonSerializer import PersonSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.security.services.UserService import UserService
from apps.security.entity.serializers.UserSerializer import UserSerializer
from apps.security.emails.SendEmails import enviar_registro_pendiente
from datetime import datetime


class PersonViewSet(BaseViewSet):
    service_class = PersonService
    serializer_class = PersonSerializer

    @action(detail=False, methods=['post'], url_path='register-aprendiz')
    def register_aprendiz(self, request):
        """
        Orquesta el registro de aprendiz, delegando toda la lógica al servicio.
        Solo retorna la respuesta del servicio, sin lógica adicional.
        """
        result = self.service.register_aprendiz(request.data)
        return Response(result['data'], status=result['status'])
