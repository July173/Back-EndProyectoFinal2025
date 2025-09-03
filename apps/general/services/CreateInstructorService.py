from django.db import transaction
from django.utils import timezone
from apps.general.repositories.CreateInstructorRepository import CreateInstructorRepository
from apps.general.entity.models import Sede, Center, Regional, PersonSede, KnowledgeArea
from apps.security.entity.models import User
from apps.general.entity.models import Instructor
from apps.general.email.SendEmailsDesactivate import enviar_desactivacion_usuario


class CreateInstructorService:
    def __init__(self):
        self.repo = CreateInstructorRepository()

    def create_instructor(self, person_data, user_data, instructor_data, sede_id, center_id, regional_id):
        with transaction.atomic():
            # Validar y obtener entidades relacionadas usando el ORM de Django
            regional = Regional.objects.get(id=regional_id)
            center = Center.objects.get(id=center_id, regional=regional)
            sede = Sede.objects.get(id=sede_id, center=center)

            # Crear Person
            person = self.repo.create_person(person_data)

            # Relacionar Person con Sede (tabla pivote)
            PersonSede.objects.create(PersonId=person, SedeId=sede)

            # Crear User (role_id=3, password=number_identification)
            user_data['person_id'] = person.id
            user_data['password'] = person_data['number_identification']  # Asigna la contraseña automáticamente
            user = self.repo.create_user(user_data)

            # Obtener instancia de KnowledgeArea
            knowledge_area_id = instructor_data.pop('knowledgeArea')
            knowledge_area_instance = KnowledgeArea.objects.get(pk=knowledge_area_id)
            instructor_data['knowledgeArea'] = knowledge_area_instance

            # Crear Instructor
            instructor_data['person'] = person  # Relación correcta
            instructor_data.pop('user_id', None)  # Elimina si existe
            instructor = self.repo.create_instructor(instructor_data)

            return {
                "person_id": person.id,
                "user_id": user.id,
                "instructor_id": instructor.id,
                "sede_id": sede.id,
                "center_id": center.id,
                "regional_id": regional.id
            }

    def update_instructor(self, instructor_id, person_data, user_data, instructor_data, sede_id):
        with transaction.atomic():
            instructor = Instructor.objects.get(pk=instructor_id)
            person = instructor.person
            user = User.objects.filter(person=person).first()

            self.repo.update_person(person, person_data)
            if user:
                self.repo.update_user(user, user_data)

            # Convierte el ID en instancia si existe en instructor_data
            if 'knowledgeArea' in instructor_data:
                knowledge_area_id = instructor_data.pop('knowledgeArea')
                instructor_data['knowledgeArea'] = KnowledgeArea.objects.get(pk=knowledge_area_id)

            self.repo.update_instructor(instructor, instructor_data)
            if sede_id:
                self.repo.update_person_sede(person, sede_id)

            return {
                "person_id": person.id,
                "user_id": user.id if user else None,
                "instructor_id": instructor.id,
                "sede_id": sede_id
            }

    def delete_instructor(self, instructor_id):
        with transaction.atomic():
            instructor = Instructor.objects.get(pk=instructor_id)
            person = instructor.person

            self.repo.delete_instructor(instructor)
            self.repo.delete_user_by_person(person)
            self.repo.delete_person_sede_by_person(person)
            self.repo.delete_person(person)

    def logical_delete_instructor(self, instructor_id):
        with transaction.atomic():
            instructor = Instructor.objects.get(pk=instructor_id)
            person = instructor.person
            user = User.objects.filter(person=person).first()

            # Si está desactivado, reactívalo y borra la fecha de eliminación
            if not instructor.active:
                instructor.active = True
                instructor.delete_at = None
                instructor.save()

                if user:
                    user.is_active = True
                    user.deleted_at = None
                    user.save()

                person.active = True
                person.delete_at = None
                person.save()

                person_sede = PersonSede.objects.filter(PersonId=person)
                for ps in person_sede:
                    ps.DeleteAt = None
                    ps.save()
                return "Instructor reactivado correctamente."

            # Si está activo, desactívalo y registra la fecha de eliminación
            self.repo.deactivate_instructor(instructor)
            self.repo.deactivate_user_by_person(person)
            self.repo.deactivate_person(person)
            self.repo.deactivate_person_sede_by_person(person)
            # Enviar correo de desactivación si existe usuario
            if user:
                nombre = f"{person.first_name} {person.second_name} {person.first_last_name} {person.second_last_name}"
                enviar_desactivacion_usuario(
                    user.email,
                    nombre,
                    timezone.now()
                )
            return "Eliminación lógica realizada correctamente."
