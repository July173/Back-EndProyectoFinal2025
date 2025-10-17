from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Apprentice
from apps.security.entity.models import Person, User
from django.utils import timezone
from django.db import transaction

class ApprenticeRepository(BaseRepository):
    """
    Repository for managing apprentice creation, update, deletion, and activation logic.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """

    def __init__(self):
        super().__init__(Apprentice)

    def create_all_dates_apprentice(self, person_data, user_data, file):
        """
        Create person, user, and apprentice in a single transaction.
        Returns apprentice, user, and person.
        """
        with transaction.atomic():
            person = Person.objects.create(**person_data)
            if User.objects.filter(email=user_data['email']).exists():
                raise ValueError("El correo ya está registrado.")
            email = user_data.pop('email')
            password = user_data.pop('password')
            user_data.pop('person_id', None)
            user = User.objects.create_user(email=email, password=password, person=person, **user_data)
            user.registered = False
            user.save()
            apprentice = Apprentice.objects.create(person_id=person, ficha_id=file)
            return apprentice, user, person

    def update_all_dates_apprentice(self, apprentice, person_data, user_data, file):
        """
        Update person, user, and apprentice in a single transaction.
        """
        with transaction.atomic():
            # Update person
            for attr, value in person_data.items():
                setattr(apprentice.person, attr, value)
            apprentice.person.save()
            # Update user
            user = User.objects.filter(person=apprentice.person).first()
            if user:
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()
            # Update apprentice
            apprentice.ficha = file
            apprentice.save()
            return apprentice

