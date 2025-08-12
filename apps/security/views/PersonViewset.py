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
        data = request.data
        email = data.get('email')
        password = data.get('password')
        # Validar correo institucional
        if not email or not email.endswith('@soy.sena.edu.co'):
            return Response({'error': 'Solo se permiten correos institucionales'}, status=status.HTTP_400_BAD_REQUEST)
        # Crear persona
        person_serializer = self.get_serializer(data=data)
        if person_serializer.is_valid():
            person = person_serializer.save()
            # Crear usuario asociado
            user_data = {
                'email': email,
                'password': password,
                'person': person.id,  # Si tienes relación en el modelo User
                'is_active': False,   # Usuario inactivo por defecto
                'role': 1,            # Rol aprendiz por defecto
            }
            user_service = UserService()
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                # Solo enviar correo si ambos se crearon correctamente
                fecha_registro = datetime.now().strftime('%d/%m/%Y')
                enviar_registro_pendiente(email, person.first_name + ' ' + person.first_last_name, fecha_registro)
                return Response({
                    'persona': person_serializer.data,
                    'usuario': user_serializer.data,
                    'success': 'Usuario registrado correctamente. Tu cuenta está pendiente de activación.'
                }, status=status.HTTP_201_CREATED)
            else:
                person.delete()  # Rollback si falla usuario
                return Response({'error': 'No se pudo crear el usuario', 'detalle': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Retornar errores detallados del serializer
            return Response({'error': 'Datos inválidos', 'detalle': person_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
