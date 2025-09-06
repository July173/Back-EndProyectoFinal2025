from django.db import transaction
from apps.general.repositories.CreateAprendizRepository import CreateAprendizRepository
from apps.security.entity.models import User, Role
from apps.general.entity.models import Aprendiz, Ficha
from apps.security.emails.CreacionCuentaUsers import send_account_created_email


class CreateAprendizService:
    def __init__(self):
        self.repo = CreateAprendizRepository()

    def create_aprendiz(self, person_data, user_data, ficha_id):
        with transaction.atomic():
            person = self.repo.create_person(person_data)
            user_data['person_id'] = person.id
            user_data['password'] = person_data['number_identification']  # Asigna la contraseña automáticamente
            # Assign default role id=2 if not provided
            if not user_data.get('role_id'):
                try:
                    default_role = Role.objects.get(pk=2)
                    user_data['role_id'] = default_role.id
                except Role.DoesNotExist:
                    # If default role doesn't exist, continue without setting role
                    pass

            email = user_data.get('email')
            temp_password = user_data.get('password')
            user = self.repo.create_user(user_data)
            # send email with temporary password (non-blocking)
            try:
                full_name = f"{person.first_name} {person.first_last_name}"
                send_account_created_email(email, full_name, temp_password)
            except Exception:
                # logging is handled inside send_account_created_email
                pass
            ficha = Ficha.objects.get(pk=ficha_id)
            aprendiz = self.repo.create_aprendiz(person, ficha)
            return aprendiz

    def update_aprendiz(self, aprendiz_id, person_data, user_data, ficha_id, role_id):
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            person = aprendiz.person
            user = User.objects.filter(person=person).first()
            ficha = Ficha.objects.get(pk=ficha_id)
            # Use provided role_id or fallback to default role id=2
            if not role_id:
                role_id = 2

            try:
                role = Role.objects.get(pk=role_id)
            except Role.DoesNotExist:
                role = None

            self.repo.update_person(person, person_data)
            if user:
                if role:
                    user_data['role_id'] = role.id
                else:
                    # if role lookup failed, ensure there's still a numeric id fallback
                    user_data['role_id'] = 2
                self.repo.update_user(user, user_data)
            self.repo.update_aprendiz(aprendiz, ficha)
            return aprendiz

    def delete_aprendiz(self, aprendiz_id):
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            person = aprendiz.person
            self.repo.delete_aprendiz(aprendiz)
            self.repo.delete_user_by_person(person)
            self.repo.delete_person(person)

    def logical_delete_aprendiz(self, aprendiz_id):
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            person = aprendiz.person
            user = User.objects.filter(person=person).first()

            if not aprendiz.active:
                self.repo.activate_aprendiz(aprendiz)
                self.repo.activate_user_by_person(person)
                self.repo.activate_person(person)
                return "Aprendiz reactivado correctamente."
            else:
                self.repo.deactivate_aprendiz(aprendiz)
                self.repo.deactivate_user_by_person(person)
                self.repo.deactivate_person(person)
                return "Eliminación lógica realizada correctamente."
