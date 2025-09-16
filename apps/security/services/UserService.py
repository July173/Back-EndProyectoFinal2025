
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
from apps.security.emails.SendEmailsDesactivate import enviar_desactivacion_usuario
from core.utils.Validation import is_soy_sena_email, is_sena_email


class UserService(BaseService):
    def update(self, pk, data):
        # Si se envía una nueva contraseña, hashearla antes de actualizar
        pwd = data.get('password')
        if pwd:
            data['password'] = make_password(pwd)
        return super().update(pk, data)
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
        if not (is_soy_sena_email(email) or is_sena_email(email)):
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
        if not (is_soy_sena_email(email) or is_sena_email(email)):
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
        print("userrr **** info xxxx : ", user.person.id)
        # Generar JWT
        refresh = RefreshToken.for_user(user)
        return {
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'email': user.email,
                    'id': user.id,
                    'role': user.role.id if user.role else None,
                    'person': user.person.id if user.person else None,  # Solo el id
                    'registered': user.registered if hasattr(user, 'registered') else None
                }
            },
            'status': status.HTTP_200_OK
        }

    def soft_delete(self, pk, motivo="Desactivación de cuenta"):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return False

        # Si el usuario está desactivado (deleted_at lleno o is_active False) -> restaurar
        is_deactivated = False
        if hasattr(user, 'is_active'):
            is_deactivated = not user.is_active
        elif hasattr(user, 'active'):
            is_deactivated = not user.active
        else:
            is_deactivated = getattr(user, 'deleted_at', None) is not None

        if is_deactivated:
            # Restaurar
            if hasattr(user, 'restore'):
                user.restore()
            else:
                # Fallback manual
                if hasattr(user, 'is_active'):
                    user.is_active = True
                if hasattr(user, 'active'):
                    user.active = True
                if hasattr(user, 'deleted_at'):
                    user.deleted_at = None
                if hasattr(user, 'delete_at'):
                    user.delete_at = None
                user.save()
            # Marcar como activado
            user.registered = False
            user.save()
            # Enviar correo de activación con el correo y contraseña actual
            from apps.security.emails.SendEmailsActivate import enviar_activacion_usuario
            nombre = f"{user.person.first_name} {user.person.first_last_name}" if user.person else user.email
            email_usuario = user.email
            # Restablecer la contraseña al número de identificación antes de enviar el correo
            numero_identificacion = None
            if user.person and hasattr(user.person, 'number_identification'):
                numero_identificacion = str(user.person.number_identification)
            if not numero_identificacion:
                numero_identificacion = '(No disponible)'
            else:
                from django.contrib.auth.hashers import make_password
                user.set_password(numero_identificacion)
                user.save()
            enviar_activacion_usuario(
                email_usuario,
                nombre,
                email_usuario,
                numero_identificacion
            )
            return True

        # Si estaba activo -> desactivar y enviar correo
        # Usar método del modelo si existe
        if hasattr(user, 'soft_delete'):
            user.soft_delete()
        else:
            if hasattr(user, 'is_active'):
                user.is_active = False
            if hasattr(user, 'active'):
                user.active = False
            if hasattr(user, 'deleted_at'):
                user.deleted_at = timezone.now()
            if hasattr(user, 'delete_at'):
                user.delete_at = timezone.now()
            user.save()

        nombre = f"{user.person.first_name} {user.person.first_last_name}" if user.person else user.email
        fecha_desactivacion = timezone.now().strftime('%d/%m/%Y')
        enviar_desactivacion_usuario(
            user.email,
            nombre,
            fecha_desactivacion,
            motivo
        )
        return True
