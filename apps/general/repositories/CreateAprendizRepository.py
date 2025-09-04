from apps.security.entity.models import Person, User
from apps.general.entity.models import Aprendiz, Ficha, Program
from django.utils import timezone

class CreateAprendizRepository:
    def create_person(self, data):
        return Person.objects.create(**data)

    def create_user(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValueError("El correo ya está registrado.")
        email = data.pop('email')
        password = data.pop('password')
        return User.objects.create_user(email=email, password=password, **data)

    def create_aprendiz(self, person, ficha):
        return Aprendiz.objects.create(person=person, ficha=ficha)

    def update_person(self, person, data):
        for attr, value in data.items():
            setattr(person, attr, value)
        person.save()
        return person

    def update_user(self, user, data):
        for attr, value in data.items():
            setattr(user, attr, value)
        user.save()
        return user

    def update_aprendiz(self, aprendiz, ficha):
        aprendiz.ficha = ficha
        aprendiz.save()
        return aprendiz

    def delete_aprendiz(self, aprendiz):
        aprendiz.delete()

    def delete_user_by_person(self, person):
        user = User.objects.filter(person=person).first()
        if user:
            user.delete()

    def delete_person(self, person):
        person.delete()

    def deactivate_aprendiz(self, aprendiz):
        aprendiz.active = False
        aprendiz.delete_at = timezone.now()
        aprendiz.save()
        return aprendiz

    def activate_aprendiz(self, aprendiz):
        aprendiz.active = True
        aprendiz.delete_at = None
        aprendiz.save()
        return aprendiz

    def deactivate_user_by_person(self, person):
        user = User.objects.filter(person=person).first()
        if user:
            user.is_active = False
            user.deleted_at = timezone.now()
            user.save()
        return user

    def activate_user_by_person(self, person):
        user = User.objects.filter(person=person).first()
        if user:
            user.is_active = True
            user.deleted_at = None
            user.save()
        return user

    def deactivate_person(self, person):
        person.active = False
        person.delete_at = timezone.now()
        person.save()
        return person

    def activate_person(self, person):
        person.active = True
        person.delete_at = None
        person.save()
        return person