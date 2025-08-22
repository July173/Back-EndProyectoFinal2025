from apps.security.entity.models import Person, User
from apps.general.entity.models import Instructor


class CreateInstructorRepository:
    def create_person(self, data):
        return Person.objects.create(**data)

    def create_user(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValueError("El correo ya está registrado.")
        return User.objects.create(**data)

    def create_instructor(self, data):
        return Instructor.objects.create(**data)
