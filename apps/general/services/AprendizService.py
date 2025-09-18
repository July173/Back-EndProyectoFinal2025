from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.AprendizRepository import AprendizRepository
from apps.security.entity.models import User, Role, Person
from apps.general.entity.models import Aprendiz, Ficha
from apps.security.emails.CreacionCuentaUsers import send_account_created_email
from django.db import transaction
from core.utils.Validation import is_unique_email, is_unique_document_number, is_valid_phone_number

class AprendizService(BaseService):
    def __init__(self):
        self.repository = AprendizRepository()

    def create_aprendiz(self, validated_data):
        """
        Crea un aprendiz, usuario y persona. Valida datos y envía correo de bienvenida.
        """
        from core.utils.Validation import is_soy_sena_email
        # Construcción de datos de persona
        person_data = {
            'type_identification': validated_data['type_identification'],
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        # Construcción de datos de usuario
        user_data = {
            'email': validated_data['email'],
            'person_id': None  # Se asigna en el repo
        }
        ficha_id = validated_data['ficha_id']

        # Validación de correo institucional
        if not user_data['email'] or not is_soy_sena_email(user_data['email']):
            raise ValueError('Solo se permiten correos institucionales (@soy.sena.edu.co) para aprendices.')

        # Validaciones de unicidad y formato
        if not is_unique_email(user_data['email'], User):
            raise ValueError('El correo ya está registrado.')
        if not is_unique_document_number(person_data['number_identification'], Person):
            raise ValueError('El número de documento ya está registrado.')
        if person_data['phone_number'] and not is_valid_phone_number(person_data['phone_number']):
            raise ValueError('El número de teléfono debe tener exactamente 10 dígitos.')

        with transaction.atomic():
            # Asigna la contraseña y rol por defecto
            user_data['password'] = str(person_data['number_identification'])
            if not user_data.get('role_id'):
                try:
                    default_role = Role.objects.get(pk=2)
                    user_data['role_id'] = default_role.id
                except Role.DoesNotExist:
                    pass

            # Obtiene ficha y crea registros
            email = user_data.get('email')
            temp_password = user_data.get('password')
            ficha = Ficha.objects.get(pk=ficha_id)
            aprendiz, user, person = self.repository.create_all_dates_aprendiz(person_data, user_data, ficha)

            # Envía correo de bienvenida
            email_sent = False
            email_error = None
            try:
                if user and email and temp_password:
                    full_name = f"{person_data.get('first_name', '')} {person_data.get('first_last_name', '')}"
                    send_account_created_email(email, full_name, temp_password)
                    email_sent = True
                else:
                    email_error = f"Datos insuficientes para enviar correo: email={email}, password={temp_password}"
            except Exception as e:
                email_error = str(e)
            if not email_sent:
                print(f"[AprendizService] No se pudo enviar el correo de registro al aprendiz: {email_error}")
            return aprendiz, user, person

    def update_aprendiz(self, aprendiz_id, validated_data):
        """
        Actualiza los datos de aprendiz, usuario y persona. Valida datos y roles.
        """
        from core.utils.Validation import is_soy_sena_email
        # Construcción de datos de persona
        person_data = {
            'type_identification': validated_data['type_identification'],
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        # Construcción de datos de usuario
        user_data = {
            'email': validated_data['email'],
        }
        ficha_id = validated_data['ficha_id']
        role_id = validated_data['role_id']

        aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
        # Validación de correo institucional
        if not user_data['email'] or not is_soy_sena_email(user_data['email']):
            raise ValueError('Solo se permiten correos institucionales (@soy.sena.edu.co) para aprendices.')
        # Obtener el usuario usando la relación con la persona
        user = User.objects.filter(person=aprendiz.person).first()
        # Validaciones de unicidad y formato
        if not is_unique_email(user_data['email'], User, exclude_user_id=user.id if user else None):
            raise ValueError('El correo ya está registrado.')
        if not is_unique_document_number(person_data['number_identification'], Person, exclude_person_id=aprendiz.person.id):
            raise ValueError('El número de documento ya está registrado.')
        if person_data['phone_number'] and not is_valid_phone_number(person_data['phone_number']):
            raise ValueError('El número de teléfono debe tener exactamente 10 dígitos.')

        with transaction.atomic():
            # Actualiza ficha y rol
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            ficha = Ficha.objects.get(pk=ficha_id)
            if not role_id:
                role_id = 2
            try:
                role = Role.objects.get(pk=role_id)
                user_data['role_id'] = role.id
            except Role.DoesNotExist:
                user_data['role_id'] = 2
            self.repository.update_all_dates_aprendiz(aprendiz, person_data, user_data, ficha)
            return aprendiz

    def get_aprendiz(self, aprendiz_id):
        """
        Obtiene un aprendiz por id.
        """
        return Aprendiz.objects.filter(pk=aprendiz_id).first()

    def list_aprendices(self):
        """
        Lista todos los aprendices.
        """
        return Aprendiz.objects.all()

    def delete_aprendiz(self, aprendiz_id):
        """
        Elimina completamente un aprendiz y sus datos relacionados.
        """
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            self.repository.delete_all_dates_aprendiz(aprendiz)

    def logical_delete_aprendiz(self, aprendiz_id):
        """
        Realiza borrado lógico o reactivación de aprendiz.
        """
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            if not aprendiz.active:
                self.repository.set_active_state_dates_aprendiz(aprendiz, active=True)
                return "Aprendiz reactivado correctamente."
            else:
                self.repository.set_active_state_dates_aprendiz(aprendiz, active=False)
                return "Eliminación lógica realizada correctamente."
