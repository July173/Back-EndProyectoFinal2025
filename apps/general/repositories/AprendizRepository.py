from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Aprendiz, Ficha, Program
from apps.security.entity.models import Person, User
from django.utils import timezone

class AprendizRepository(BaseRepository):
    def __init__(self):
        super().__init__(Aprendiz)

    def create_all_dates_aprendiz(self, person_data, user_data, ficha):
        """
        Crea persona, usuario y aprendiz en una sola transacción.
        Retorna aprendiz, user y person.
        """
        from django.db import transaction
        with transaction.atomic():
            person = Person.objects.create(**person_data)
            if User.objects.filter(email=user_data['email']).exists():
                raise ValueError("El correo ya está registrado.")
            email = user_data.pop('email')
            password = user_data.pop('password')
            # Eliminar person_id si existe en user_data para evitar sobrescribir el valor correcto
            user_data.pop('person_id', None)
            user = User.objects.create_user(email=email, password=password, person=person, **user_data)
            aprendiz = Aprendiz.objects.create(person=person, ficha=ficha)
            return aprendiz, user, person

    def update_all_dates_aprendiz(self, aprendiz, person_data, user_data, ficha):
        """
        Actualiza persona, usuario y aprendiz en una sola transacción.
        """
        from django.db import transaction
        with transaction.atomic():
            # Persona
            for attr, value in person_data.items():
                setattr(aprendiz.person, attr, value)
            aprendiz.person.save()
            # Usuario
            user = User.objects.filter(person=aprendiz.person).first()
            if user:
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()
            # Aprendiz
            aprendiz.ficha = ficha
            aprendiz.save()
            return aprendiz

    def delete_all_dates_aprendiz(self, aprendiz):
        """
        Elimina aprendiz, usuario y persona en cascada.
        """
        from django.db import transaction
        with transaction.atomic():
            person = aprendiz.person
            user = User.objects.filter(person=person).first()
            aprendiz.delete()
            if user:
                user.delete()
            person.delete()

    def set_active_state_dates_aprendiz(self, aprendiz, active=True):
        """
        Activa o desactiva aprendiz, usuario y persona en cascada.
        """
        from django.db import transaction
        with transaction.atomic():
            aprendiz.active = active
            aprendiz.delete_at = None if active else timezone.now()
            aprendiz.save()
            person = aprendiz.person
            person.active = active
            person.delete_at = None if active else timezone.now()
            person.save()
            user = User.objects.filter(person=person).first()
            if user:
                user.is_active = active
                user.deleted_at = None if active else timezone.now()
                user.save()
            return aprendiz
