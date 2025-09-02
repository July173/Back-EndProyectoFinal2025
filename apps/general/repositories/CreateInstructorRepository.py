from apps.security.entity.models import Person, User
from apps.general.entity.models import Instructor, PersonSede, Sede
from django.utils import timezone


class CreateInstructorRepository:
    def create_person(self, data):
        return Person.objects.create(**data)

    def update_person(self, person, data):
        for attr, value in data.items():
            setattr(person, attr, value)
        person.save()
        return person

    def create_user(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValueError("El correo ya está registrado.")
        email = data.pop('email')
        password = data.pop('password')
        return User.objects.create_user(email=email, password=password, **data)

    def update_user(self, user, data):
        for attr, value in data.items():
            setattr(user, attr, value)
        user.save()
        return user

    def create_instructor(self, data):
        return Instructor.objects.create(**data)

    def update_instructor(self, instructor, data):
        for attr, value in data.items():
            setattr(instructor, attr, value)
        instructor.save()
        return instructor

    def update_person_sede(self, person, sede_id):
        sede_instance = Sede.objects.get(pk=sede_id)
        person_sede = PersonSede.objects.filter(PersonId=person).first()
        if person_sede:
            person_sede.SedeId = sede_instance
            person_sede.save()
        return person_sede

    def delete_instructor(self, instructor):
        instructor.delete()

    def delete_user_by_person(self, person):
        user = User.objects.filter(person=person).first()
        if user:
            user.delete()

    def delete_person_sede_by_person(self, person):
        person_sede = PersonSede.objects.filter(PersonId=person)
        person_sede.delete()

    def delete_person(self, person):
        person.delete()

    def deactivate_instructor(self, instructor):
        instructor.active = False
        instructor.delete_at = timezone.now()  # <-- minúscula, como en el modelo
        instructor.save()
        return instructor

    def deactivate_user_by_person(self, person):
        user = User.objects.filter(person=person).first()
        if user:
            user.is_active = False
            user.deleted_at = timezone.now()  # <-- como en el modelo User
            user.save()
        return user

    def deactivate_person(self, person):
        person.active = False
        person.delete_at = timezone.now()  # <-- minúscula, como en el modelo
        person.save()
        return person

    def deactivate_person_sede_by_person(self, person):
        person_sede = PersonSede.objects.filter(PersonId=person)
        for ps in person_sede:
            # Si tienes campo active en PersonSede, desactívalo también
            if hasattr(ps, 'active'):
                ps.active = False
            ps.DeleteAt = timezone.now()  # <-- respeta la mayúscula
            ps.save()
        return person_sede
