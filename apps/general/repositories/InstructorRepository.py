from django.db.models import Q
from apps.security.entity.models.DocumentType import DocumentType
from apps.security.entity.models.Role import Role
from django.utils import timezone
from apps.security.entity.models import Person, User
from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Instructor, PersonSede, Sede
from apps.general.entity.models.TypeContract import TypeContract
from django.db import transaction

class InstructorRepository(BaseRepository):
    """
    Optimized repository for CRUD and state operations on Instructor, Person, User, and PersonSede.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """

    def get_filtered_instructors(self, search=None, knowledge_area_id=None):
        """
        Get instructors filtered by search text and/or knowledge area ID.
        """
        queryset = self.model.objects.select_related('person', 'knowledgeArea').all()
        if search:
            queryset = queryset.filter(
                Q(person__first_name__icontains=search) |
                Q(person__second_name__icontains=search) |
                Q(person__first_last_name__icontains=search) |
                Q(person__second_last_name__icontains=search) |
                Q(person__number_identification__icontains=search)
            )
        if knowledge_area_id:
            queryset = queryset.filter(knowledgeArea__id=knowledge_area_id)
        return list(queryset)

    def __init__(self):
        super().__init__(Instructor)

    def create_all_dates_instructor(self, person_data, user_data, instructor_data, sede_id=None):
        """
        Create person, user, instructor, and person_sede in a single transaction.
        Returns instructor, user, person, person_sede.
        """
        with transaction.atomic():
            if isinstance(person_data.get('type_identification'), int):
                person_data['type_identification'] = DocumentType.objects.get(pk=person_data['type_identification'])
            person = Person.objects.create(**person_data)
            # Convert role_id to Role instance if present (assume valid)
            if 'role_id' in user_data:
                role_id = user_data['role_id']
                if role_id and int(role_id) > 0:
                    user_data['role'] = Role.objects.get(pk=role_id)
                user_data.pop('role_id')
            if User.objects.filter(email=user_data['email']).exists():
                # User-facing error message remains in Spanish
                raise ValueError("El correo ya está registrado.")
            email = user_data.pop('email')
            password = user_data.pop('password')
            user = User.objects.create_user(email=email, password=password, person=person, **user_data)
            user.registered = False
            user.save()
            if isinstance(instructor_data.get('contract_type'), int):
                instructor_data['contract_type'] = TypeContract.objects.get(pk=instructor_data['contract_type'])
            instructor = Instructor.objects.create(person=person, **instructor_data)
            person_sede = None
            if sede_id:
                sede_instance = Sede.objects.get(pk=sede_id)
                person_sede = PersonSede.objects.create(person_id=person, sede_id=sede_instance)
            return instructor, user, person, person_sede

    def update_all_dates_instructor(self, instructor, person_data, user_data, instructor_data, sede_id=None):
        """
        Update person, user, instructor, and person_sede in a single transaction.
        """
        with transaction.atomic():
            # Update person
            for attr, value in person_data.items():
                setattr(instructor.person, attr, value)
            instructor.person.save()
            # Update user
            user = User.objects.filter(person=instructor.person).first()
            if user:
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()
            # Update instructor
            for attr, value in instructor_data.items():
                setattr(instructor, attr, value)
            instructor.save()
            # Update person_sede
            if sede_id:
                sede_instance = Sede.objects.get(pk=sede_id)
                person_sede = PersonSede.objects.filter(PersonId=instructor.person).first()
                if person_sede:
                    person_sede.SedeId = sede_instance
                    person_sede.save()
            return instructor

    def delete_all_dates_instructor(self, instructor):
        """
        Delete instructor, user, person_sede, and person in cascade.
        """
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
        Activate or deactivate instructor, user, person, and person_sede in cascade.
        """
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
                # Respect uppercase/lowercase according to the model
                if hasattr(ps, 'DeleteAt'):
                    ps.DeleteAt = None if active else timezone.now()
                elif hasattr(ps, 'delete_at'):
                    ps.delete_at = None if active else timezone.now()
                ps.save()
            return instructor

    
