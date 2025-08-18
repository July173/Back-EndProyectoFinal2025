from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.UserRepository import UserRepository
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from apps.security.entity.models import User
class UserService(BaseService):
    def reset_password(self, email, new_password):
        # Validar correo y nueva contraseña
        if not email or not new_password:
            return {
                'data': {'error': 'Faltan datos requeridos.'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return {
                'data': {'error': 'No existe un usuario con ese correo.'},
                'status': status.HTTP_404_NOT_FOUND
            }
        # Cambiar contraseña
        user.set_password(new_password)
        user.reset_code = None
        user.reset_code_expiration = None
        user.save()
        return {
            'data': {'success': 'Contraseña actualizada correctamente.'},
            'status': status.HTTP_200_OK
        }
    def send_password_reset_code(self, email):
            # Validar correo institucional
            if not email or not (email.endswith('@soy.sena.edu.co') or email.endswith('@sena.edu.co')):
                return {
                    'data': {'error': 'Solo se permiten correos institucionales (@soy.sena.edu.co o @sena.edu.co)'},
                    'status': status.HTTP_400_BAD_REQUEST
                }
            # Buscar usuario
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return {
                    'data': {'error': 'No existe un usuario con ese correo.'},
                    'status': status.HTTP_404_NOT_FOUND
                }
            # Generar código y expiración
            code = get_random_string(length=6, allowed_chars='0123456789')
            expiration = timezone.now() + timedelta(minutes=15)
            user.reset_code = code
            user.reset_code_expiration = expiration
            user.save()
            # Verificar que se guardó correctamente
            user_refresh = User.objects.get(email=email)
            if user_refresh.reset_code == code and user_refresh.reset_code_expiration == expiration:
                # Renderizar email solo si se guardó correctamente
                nombre = user.person.first_name if user.person else user.email
                fecha_expiracion = expiration.strftime('%d/%m/%Y %H:%M')
                html_content = render_to_string('RestablecerContraseña.html', {
                    'nombre': nombre,
                    'codigo': code,
                    'fecha_expiracion': fecha_expiracion
                })
                subject = 'Recuperación de Contraseña SENA'
                email_msg = EmailMultiAlternatives(subject, '', to=[email])
                email_msg.attach_alternative(html_content, "text/html")
                email_msg.send()
                return {
                    'data': {
                        'code': code,
                        'fecha_expiracion': fecha_expiracion,
                        'success': 'Código enviado correctamente al correo institucional.'
                    },
                    'status': status.HTTP_200_OK
                }
            else:
                return {
                    'data': {'error': 'No se pudo registrar el código de recuperación.'},
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                }
    

    def __init__(self):
        self.repository = UserRepository()

    def create(self, data):
        pwd = data.get('password')
        if pwd:
            data['password'] = make_password(pwd)
        return super().create(data)

    def change_password(self, pk, new_password):
        inst = self.get(pk)
        inst.set_password(new_password)
        inst.save()
        return inst

    def validate_institutional_login(self, email, password):
        # Validar correo institucional
        if not email or not (email.endswith('@soy.sena.edu.co') or email.endswith('@sena.edu.co')):
            return {
                'data': {'error': 'Solo se permiten correos institucionales (@soy.sena.edu.co o @sena.edu.co)'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Validar contraseña (mínimo 8 caracteres)
        if not password or len(password) < 8:
            return {
                'data': {'error': 'La contraseña debe tener al menos 8 caracteres.'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Autenticación
        user = authenticate(email=email, password=password)
        if user is None:
            return {
                'data': {'error': 'Credenciales inválidas.'},
                'status': status.HTTP_401_UNAUTHORIZED
            }
        # Generar JWT
        refresh = RefreshToken.for_user(user)
        return {
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'email': user.email,
                    'id': user.id,
                    'role': user.role.id if user.role else None,  # Solo el id
                }
            },
            'status': status.HTTP_200_OK
        }
