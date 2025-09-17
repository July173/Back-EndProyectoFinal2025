from apps.security.entity.models import Person, User
from apps.general.entity.models import Instructor, PersonSede, Sede
from django.utils import timezone


class CreateInstructorRepository:
    """
    Repositorio optimizado para operaciones CRUD y de estado sobre Instructor, Persona, Usuario y PersonSede.
    """

    def create_all_dates_instructor(self, person_data, user_data, instructor_data, sede_id=None):
        """
        Crea persona, usuario, instructor y person_sede en una sola transacción.
        Retorna instructor, user, person, person_sede.
        """
        from django.db import transaction
        with transaction.atomic():
            person = Person.objects.create(**person_data)
            if User.objects.filter(email=user_data['email']).exists():
                raise ValueError("El correo ya está registrado.")
            email = user_data.pop('email')
            password = user_data.pop('password')
            user = User.objects.create_user(email=email, password=password, person=person, **user_data)
            instructor = Instructor.objects.create(person=person, **instructor_data)
            person_sede = None
            if sede_id:
                sede_instance = Sede.objects.get(pk=sede_id)
                person_sede = PersonSede.objects.create(PersonId=person, SedeId=sede_instance)
            return instructor, user, person, person_sede

    def update_all_dates_instructor(self, instructor, person_data, user_data, instructor_data, sede_id=None):
        """
        Actualiza persona, usuario, instructor y person_sede en una sola transacción.
        """
        from django.db import transaction
        with transaction.atomic():
            # Persona
            for attr, value in person_data.items():
                setattr(instructor.person, attr, value)
            instructor.person.save()
            # Usuario
            user = User.objects.filter(person=instructor.person).first()
            if user:
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()
            # Instructor
            for attr, value in instructor_data.items():
                setattr(instructor, attr, value)
            instructor.save()
            # PersonSede
            if sede_id:
                sede_instance = Sede.objects.get(pk=sede_id)
                person_sede = PersonSede.objects.filter(PersonId=instructor.person).first()
                if person_sede:
                    person_sede.SedeId = sede_instance
                    person_sede.save()
            return instructor

    def delete_all_dates_instructor(self, instructor):
        """
        Elimina instructor, usuario, person_sede y persona en cascada.
        """
        from django.db import transaction
        with transaction.atomic():
            person = instructor.person
            user = User.objects.filter(person=person).first()
            person_sede = PersonSede.objects.filter(PersonId=person)
            instructor.delete()
            if user:
                user.delete()
            person_sede.delete()
            person.delete()

    def set_active_state_dates_instructor(self, instructor, active=True):
        """
        Activa o desactiva instructor, usuario, persona y person_sede en cascada.
        """
        from django.db import transaction
        with transaction.atomic():
            instructor.active = active
            instructor.delete_at = None if active else timezone.now()
            instructor.save()
            person = instructor.person
            person.active = active
            person.delete_at = None if active else timezone.now()
            person.save()
            user = User.objects.filter(person=person).first()
            if user:
                user.is_active = active
                user.deleted_at = None if active else timezone.now()
                user.save()
            person_sede = PersonSede.objects.filter(PersonId=person)
            for ps in person_sede:
                if hasattr(ps, 'active'):
                    ps.active = active
                # Respeta la mayúscula/minúscula según el modelo
                if hasattr(ps, 'DeleteAt'):
                    ps.DeleteAt = None if active else timezone.now()
                elif hasattr(ps, 'delete_at'):
                    ps.delete_at = None if active else timezone.now()
                ps.save()
            return instructor
