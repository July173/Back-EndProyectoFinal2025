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
from django.utils.crypto import get_random_string
from apps.security.emails.SendEmailsActivate import enviar_activacion_usuario



class UserService(BaseService):

    def __init__(self):
        self.repository = UserRepository()

    def update(self, pk, data):
        pwd = data.get('password')
        if pwd:
            data['password'] = make_password(pwd)
        try:
            return super().update(pk, data)
        except Exception as e:
            raise ValueError(f"No se pudo actualizar el usuario: {str(e)}")

    def reset_password(self, email, new_password):
        # Validate email and new password
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
        # Change password
        user.set_password(new_password)
        user.reset_code = None
        user.reset_code_expiration = None
        user.save()
        return {
            'data': {'success': 'Contraseña actualizada correctamente.'},
            'status': status.HTTP_200_OK
        }

    def send_password_reset_code(self, email):
        # Validate institutional email
        if not (is_soy_sena_email(email) or is_sena_email(email)):
            return {
                'data': {'error': 'Solo se permiten correos institucionales (@soy.sena.edu.co o @sena.edu.co)'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return {
                'data': {'error': 'No existe un usuario con ese correo.'},
                'status': status.HTTP_404_NOT_FOUND
            }
        # Generate code and expiration
        code = get_random_string(length=6, allowed_chars='0123456789')
        expiration = timezone.now() + timedelta(minutes=15)
        user.reset_code = code
        user.reset_code_expiration = expiration
        user.save()
        # Verify it was saved correctly
        user_refresh = User.objects.get(email=email)
        if user_refresh.reset_code == code and user_refresh.reset_code_expiration == expiration:
            # Render email only if saved correctly
            name = user.person.first_name if user.person else user.email
            expiration_date = expiration.strftime('%d/%m/%Y %H:%M')
            html_content = render_to_string('RestablecerContraseña.html', {
                'nombre': name,
                'codigo': code,
                'fecha_expiracion': expiration_date
            })
            subject = 'Recuperación de Contraseña SENA'
            email_msg = EmailMultiAlternatives(subject, '', to=[email])
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()
            return {
                'data': {
                    'code': code,
                    'fecha_expiracion': expiration_date,
                    'success': 'Código enviado correctamente al correo institucional.'
                },
                'status': status.HTTP_200_OK
            }
        else:
            return {
                'data': {'error': 'No se pudo registrar el código de recuperación.'},
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }

    def create(self, data):
        pwd = data.get('password')
        if pwd:
            data['password'] = make_password(pwd)
        try:
            return super().create(data)
        except Exception as e:
            raise ValueError(f"No se pudo crear el usuario: {str(e)}")

    def change_password(self, pk, new_password):
        inst = self.get(pk)
        inst.set_password(new_password)
        inst.save()
        return inst

    def validate_institutional_login(self, email, password):
        # Validate institutional email
        if not (is_soy_sena_email(email) or is_sena_email(email)):
            return {
                'data': {'error': 'Solo se permiten correos institucionales (@soy.sena.edu.co o @sena.edu.co)'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Validate password (minimum 8 characters)
        if not password or len(password) < 8:
            return {
                'data': {'error': 'La contraseña debe tener al menos 8 caracteres.'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Authentication
        user = authenticate(email=email, password=password)
        if user is None:
            return {
                'data': {'error': 'Credenciales inválidas.'},
                'status': status.HTTP_401_UNAUTHORIZED
            }
        # Generate JWT
        refresh = RefreshToken.for_user(user)
        return {
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'email': user.email,
                    'id': user.id,
                    'role': user.role.id if user.role else None,
                    'person': user.person.id if user.person else None,
                    'registered': user.registered if hasattr(user, 'registered') else None
                }
            },
            'status': status.HTTP_200_OK
        }

    def soft_delete(self, pk, reason="Account deactivation"):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return False

        # If the user is deactivated (deleted_at filled or is_active False) -> restore
        is_deactivated = False
        if hasattr(user, 'is_active'):
            is_deactivated = not user.is_active
        elif hasattr(user, 'active'):
            is_deactivated = not user.active
        else:
            is_deactivated = getattr(user, 'deleted_at', None) is not None

        if is_deactivated:
            # Restore
            if hasattr(user, 'restore'):
                user.restore()
            else:
                # Manual fallback
                if hasattr(user, 'is_active'):
                    user.is_active = True
                if hasattr(user, 'active'):
                    user.active = True
                if hasattr(user, 'deleted_at'):
                    user.deleted_at = None
                if hasattr(user, 'delete_at'):
                    user.delete_at = None
                user.save()
            # Mark as activated
            user.registered = False
            user.save()
            # Send activation email with current email and password
            name = f"{user.person.first_name} {user.person.first_last_name}" if user.person else user.email
            user_email = user.email
            # Reset password to identification number + 2 random characters before sending email
            identification_number = None
            if user.person and hasattr(user.person, 'number_identification'):
                identification_number = str(user.person.number_identification)
            if not identification_number:
                new_password = '(No disponible)'
            else:
                additional_chars = get_random_string(length=2)
                new_password = identification_number + additional_chars
                user.set_password(new_password)
                user.save()
            enviar_activacion_usuario(
                user_email,
                name,
                user_email,
                new_password
            )
            return True

        # If was active -> deactivate and send email
        # Use model method if exists
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

        name = f"{user.person.first_name} {user.person.first_last_name}" if user.person else user.email
        deactivation_date = timezone.now().strftime('%d/%m/%Y')
        enviar_desactivacion_usuario(
            user.email,
            name,
            deactivation_date,
            reason
        )
        return True

    def get_filtered_users(self, role=None, search=None):
        from django.db import models
        try:
            queryset = self.repository.get_queryset()
            if role:
                queryset = queryset.filter(role__type_role__icontains=role)
            if search:
                queryset = queryset.filter(
                    models.Q(person__first_name__icontains=search) |
                    models.Q(person__second_name__icontains=search) |
                    models.Q(person__first_last_name__icontains=search) |
                    models.Q(person__second_last_name__icontains=search) |
                    models.Q(person__number_identification__icontains=search)
                )
            users = list(queryset)
            if not users:
                raise ValueError("No se encontraron usuarios con los filtros proporcionados.")
            return users
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")
