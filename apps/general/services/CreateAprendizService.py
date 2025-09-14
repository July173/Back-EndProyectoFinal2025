from django.db import transaction
from apps.general.repositories.CreateAprendizRepository import CreateAprendizRepository
from apps.security.entity.models import User, Role
from apps.general.entity.models import Aprendiz, Ficha
from apps.security.emails.CreacionCuentaUsers import send_account_created_email


class CreateAprendizService:
    def __init__(self):
        self.repo = CreateAprendizRepository()

    def create_aprendiz(self, validated_data):
        """
        Recibe los datos validados del serializer y ejecuta la lógica de creación.
        Retorna aprendiz, user y person.
        """
        person_data = {
            'type_identification': validated_data['type_identification'],
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        user_data = {
            'email': validated_data['email'],
            'person_id': None  # Se asigna en el repo
        }
        ficha_id = validated_data['ficha_id']
        with transaction.atomic():
            user_data['password'] = person_data['number_identification']  # Asigna la contraseña automáticamente
            # Assign default role id=2 if not provided
            if not user_data.get('role_id'):
                try:
                    default_role = Role.objects.get(pk=2)
                    user_data['role_id'] = default_role.id
                except Role.DoesNotExist:
                    pass

            email = user_data.get('email')
            temp_password = user_data.get('password')
            ficha = Ficha.objects.get(pk=ficha_id)
            aprendiz, user, person = self.repo.create_all_dates_aprendiz(person_data, user_data, ficha)
            # send email with temporary password (non-blocking)
            try:
                full_name = f"{person_data.get('first_name', '')} {person_data.get('first_last_name', '')}"
                send_account_created_email(email, full_name, temp_password)
            except Exception:
                pass
            return aprendiz, user, person

    def update_aprendiz(self, aprendiz_id, validated_data):
        """
        Recibe los datos validados del serializer y ejecuta la lógica de actualización.
        """
        person_data = {
            'type_identification': validated_data['type_identification'],
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        user_data = {
            'email': validated_data['email'],
        }
        ficha_id = validated_data['ficha_id']
        role_id = validated_data['role_id']
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            ficha = Ficha.objects.get(pk=ficha_id)
            if not role_id:
                role_id = 2
            try:
                role = Role.objects.get(pk=role_id)
                user_data['role_id'] = role.id
            except Role.DoesNotExist:
                user_data['role_id'] = 2
            self.repo.update_all_dates_aprendiz(aprendiz, person_data, user_data, ficha)
            return aprendiz

    def get_aprendiz(self, aprendiz_id):
        """
        Devuelve el aprendiz por id o None si no existe.
        """
        return Aprendiz.objects.filter(pk=aprendiz_id).first()

    def list_aprendices(self):
        """
        Devuelve todos los aprendices.
        """
        return Aprendiz.objects.all()
    def __init__(self):
        self.repo = CreateAprendizRepository()



    def delete_aprendiz(self, aprendiz_id):
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            self.repo.delete_all_dates_aprendiz(aprendiz)

    def logical_delete_aprendiz(self, aprendiz_id):
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            if not aprendiz.active:
                self.repo.set_active_state_dates_aprendiz(aprendiz, active=True)
                return "Aprendiz reactivado correctamente."
            else:
                self.repo.set_active_state_dates_aprendiz(aprendiz, active=False)
                return "Eliminación lógica realizada correctamente."
