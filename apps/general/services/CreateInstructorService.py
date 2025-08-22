from django.db import transaction
from apps.general.repositories.CreateInstructorRepository import CreateInstructorRepository
from apps.general.entity.models import Sede, Center, Regional, PersonSede


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
            user = self.repo.create_user(user_data)

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
