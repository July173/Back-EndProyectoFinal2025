from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Aprendiz
from apps.security.entity.models import Person, User
from django.utils import timezone
from django.db import transaction

class AprendizRepository(BaseRepository):
    
    def __init__(self):
        super().__init__(Aprendiz)

    def create_all_dates_apprentice(self, person_data, user_data, file):
        """
        Crea persona, usuario y aprendiz en una sola transacción.
        Retorna aprendiz, user y person.
        """
        
        with transaction.atomic():
            person = Person.objects.create(**person_data)
            if User.objects.filter(email=user_data['email']).exists():
                raise ValueError("El correo ya está registrado.")
            email = user_data.pop('email')
            password = user_data.pop('password')
            # Eliminar person_id si existe en user_data para evitar sobrescribir el valor correcto
            user_data.pop('person_id', None)
            user = User.objects.create_user(email=email, password=password, person=person, **user_data)
            user.registered = False
            user.save()
            apprentice = Aprendiz.objects.create(person=person, ficha=file)
            return apprentice, user, person

    def update_all_dates_apprentice(self, apprentice, person_data, user_data, file):
        """
        Actualiza persona, usuario y aprendiz en una sola transacción.
        """

        with transaction.atomic():
            # Persona
            for attr, value in person_data.items():
                setattr(apprentice.person, attr, value)
            apprentice.person.save()
            # Usuario
            user = User.objects.filter(person=apprentice.person).first()
            if user:
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()
            # Aprendiz
            apprentice.ficha = file
            apprentice.save()
            return apprentice

    def delete_all_dates_apprentice(self, apprentice):
        """
        Elimina aprendiz, usuario y persona en cascada.
        """

        with transaction.atomic():
            person = apprentice.person
            user = User.objects.filter(person=person).first()
            apprentice.delete()
            if user:
                user.delete()
            person.delete()

    def set_active_state_dates_apprentice(self, apprentice, active=True):
        """
        Activa o desactiva aprendiz, usuario y persona en cascada.
        """

        with transaction.atomic():
            apprentice.active = active
            apprentice.delete_at = None if active else timezone.now()
            apprentice.save()
            person = apprentice.person
            person.active = active
            person.delete_at = None if active else timezone.now()
            person.save()
            user = User.objects.filter(person=person).first()
            if user:
                user.is_active = active
                user.deleted_at = None if active else timezone.now()
                user.save()
            return apprentice


