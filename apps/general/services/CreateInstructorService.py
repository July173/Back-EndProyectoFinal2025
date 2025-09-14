from django.db import transaction
from apps.general.repositories.CreateInstructorRepository import CreateInstructorRepository
from apps.general.entity.models import Sede, Center, Regional, PersonSede, KnowledgeArea
from apps.security.entity.models import User
from apps.general.entity.models import Instructor
from apps.security.emails.CreacionCuentaUsers import send_account_created_email


class CreateInstructorService:

    def list_instructors(self):
        """
        Devuelve todos los instructores.
        """
        return Instructor.objects.all()

    def get_instructor(self, instructor_id):
        """
        Devuelve el instructor por id o None si no existe.
        """
        return Instructor.objects.filter(pk=instructor_id).first()
    def __init__(self):
        self.repo = CreateInstructorRepository()

    def create_instructor(self, person_data, user_data, instructor_data, sede_id, center_id, regional_id):
        with transaction.atomic():
            # Validar y obtener entidades relacionadas usando el ORM de Django
            regional = Regional.objects.get(id=regional_id)
            center = Center.objects.get(id=center_id, regional=regional)
            sede = Sede.objects.get(id=sede_id, center=center)

            # Preparar datos para KnowledgeArea
            knowledge_area_id = instructor_data.pop('knowledgeArea')
            knowledge_area_instance = KnowledgeArea.objects.get(pk=knowledge_area_id)
            instructor_data['knowledgeArea'] = knowledge_area_instance

            # Preparar datos para user
            user_data['password'] = person_data['number_identification']  # Asigna la contraseña automáticamente

            # Crear todo en una sola transacción
            instructor, user, person, person_sede = self.repo.create_all_dates_instructor(
                person_data, user_data, instructor_data, sede_id=sede.id
            )

            # send creation email (non-blocking)
            try:
                full_name = f"{person.first_name} {person.first_last_name}"
                send_account_created_email(user.email, full_name, user_data['password'])
            except Exception:
                pass

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
            # Convierte el ID en instancia si existe en instructor_data
            if 'knowledgeArea' in instructor_data:
                knowledge_area_id = instructor_data.pop('knowledgeArea')
                instructor_data['knowledgeArea'] = KnowledgeArea.objects.get(pk=knowledge_area_id)

            self.repo.update_all_dates_instructor(
                instructor,
                person_data,
                user_data,
                instructor_data,
                sede_id=sede_id
            )
            person = instructor.person
            user = User.objects.filter(person=person).first()
            return {
                "person_id": person.id,
                "user_id": user.id if user else None,
                "instructor_id": instructor.id,
                "sede_id": sede_id
            }

    def delete_instructor(self, instructor_id):
        with transaction.atomic():
            instructor = Instructor.objects.get(pk=instructor_id)
            self.repo.delete_all_dates_instructor(instructor)

    def logical_delete_instructor(self, instructor_id):
        with transaction.atomic():
            instructor = Instructor.objects.get(pk=instructor_id)
            if not instructor.active:
                instructor.active = True
                instructor.delete_at = None
                instructor.save()
                person = instructor.person
                user = User.objects.filter(person=person).first()
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
            self.repo.set_active_state_dates_instructor(instructor, active=False)
            return "Eliminación lógica realizada correctamente."
