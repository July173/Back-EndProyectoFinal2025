from django.db import transaction
from django.utils import timezone
from apps.general.email.SendEmailsDesactivate import enviar_desactivacion_usuario
from apps.general.repositories.CreateAprendizRepository import CreateAprendizRepository
from apps.security.entity.models import User, Role
from apps.general.entity.models import Aprendiz, Ficha

class CreateAprendizService:
    def __init__(self):
        self.repo = CreateAprendizRepository()

    def create_aprendiz(self, person_data, user_data, ficha_id):
        with transaction.atomic():
            person = self.repo.create_person(person_data)
            user_data['person_id'] = person.id
            user_data['password'] = person_data['number_identification']  # Asigna la contraseña automáticamente
            self.repo.create_user(user_data)
            ficha = Ficha.objects.get(pk=ficha_id)
            aprendiz = self.repo.create_aprendiz(person, ficha)
            return aprendiz

    def update_aprendiz(self, aprendiz_id, person_data, user_data, ficha_id, role_id):
        with transaction.atomic():
            aprendiz = Aprendiz.objects.get(pk=aprendiz_id)
            person = aprendiz.person
            user = User.objects.filter(person=person).first()
            ficha = Ficha.objects.get(pk=ficha_id)
            role = Role.objects.get(pk=role_id)

            self.repo.update_person(person, person_data)
            if user:
                user_data['role_id'] = role.id
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
                # Enviar correo de desactivación si existe usuario
                if user:
                    nombre = f"{person.first_name} {person.second_name} {person.first_last_name} {person.second_last_name}"
                    enviar_desactivacion_usuario(
                        user.email,
                        nombre,
                        timezone.now()
                    )
                return "Eliminación lógica realizada correctamente."