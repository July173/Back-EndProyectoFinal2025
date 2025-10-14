from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.InstructorRepository import InstructorRepository
from django.db import transaction
from apps.general.entity.models import Sede, Center, Regional, PersonSede, KnowledgeArea
from apps.security.entity.models import User, Person
from apps.general.entity.models import Instructor
from apps.security.emails.CreacionCuentaUsers import send_account_created_email
from core.utils.Validation import is_unique_email, is_unique_document_number, is_valid_phone_number
from django.utils.crypto import get_random_string
from core.utils.Validation import is_sena_email
from django.core.exceptions import ObjectDoesNotExist

class InstructorService(BaseService):
    """
    Service for managing instructor creation, update, deletion, and activation logic.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """

    def update_learners_fields(self, instructor_id, assigned_learners=None, max_assigned_learners=None):
        """
        Update assigned_learners and max_assigned_learners fields for an instructor.
        Validates that assigned_learners is not negative and does not exceed the maximum limit.
        """
        instructor = Instructor.objects.filter(pk=instructor_id).first()
        if not instructor:
            return None
        # Validation: assigned_learners must never be less than 0
        if assigned_learners is not None:
            if assigned_learners < 0:
                raise ValueError('El número de aprendices asignados no puede ser menor que 0.')
            # Validation: do not exceed the limit
            max_limit = max_assigned_learners if max_assigned_learners is not None else instructor.max_assigned_learners or 80
            if assigned_learners > max_limit:
                raise ValueError('El número de aprendices asignados no puede superar el límite máximo.')
            instructor.assigned_learners = assigned_learners
        if max_assigned_learners is not None:
            if max_assigned_learners < 0:
                raise ValueError('El límite máximo no puede ser menor que 0.')
            instructor.max_assigned_learners = max_assigned_learners
            # If the limit is reduced below assigned, adjust assigned
            if instructor.assigned_learners is not None and instructor.assigned_learners > max_assigned_learners:
                instructor.assigned_learners = max_assigned_learners
        instructor.save()
        return instructor

    def __init__(self):
        self.repository = InstructorRepository()

    def list_instructors(self):
        """
        Return all instructors.
        """
        return Instructor.objects.all()

    def get_instructor(self, instructor_id):
        """
        Return the instructor by ID or None if not found.
        """
        return Instructor.objects.filter(pk=instructor_id).first()

    def create_instructor(self, person_data, user_data, instructor_data, sede_id):
        """
        Create an instructor, user, person, and person_sede. Validate data and send welcome email.
        """
        with transaction.atomic():
            # Get the site and its relations
            try:
                sede = Sede.objects.get(id=sede_id)
            except ObjectDoesNotExist:
                raise ValueError(f'Site with id {sede_id} does not exist.')

            # Prepare data for KnowledgeArea
            knowledge_area_id = instructor_data.pop('knowledgeArea')
            knowledge_area_instance = KnowledgeArea.objects.get(pk=knowledge_area_id)
            instructor_data['knowledgeArea'] = knowledge_area_instance

            # Handle new optional fields
            assigned_learners = instructor_data.pop('assigned_learners', None)
            max_assigned_learners = instructor_data.pop('max_assigned_learners', 80)
            instructor_data['assigned_learners'] = assigned_learners
            instructor_data['max_assigned_learners'] = max_assigned_learners

            # Prepare data for user
            numero_identificacion = str(person_data['number_identification'])
            caracteres_adicionales = get_random_string(length=2)
            password_temporal = numero_identificacion + caracteres_adicionales
            user_data['password'] = password_temporal
            temp_email = user_data.get('email')
            temp_password = password_temporal

            # Institutional email validation @sena.edu.co
            if not temp_email or not is_sena_email(temp_email):
                raise ValueError('Solo se permiten correos institucionales (@sena.edu.co) para instructores.')

            # Reusable validations
            if not is_unique_email(user_data['email'], User):
                raise ValueError('El correo ya está registrado.')
            if not is_unique_document_number(person_data['number_identification'], Person):
                raise ValueError('El número de documento ya está registrado.')
            if person_data.get('phone_number') and not is_valid_phone_number(person_data['phone_number']):
                raise ValueError('El número de teléfono debe tener exactamente 10 dígitos.')

            # Create everything in a single transaction
            instructor, user, person, person_sede = self.repository.create_all_dates_instructor(
                person_data, user_data, instructor_data, sede_id=sede.id
            )

            # Validate data before sending email
            email_sent = False
            email_error = None
            try:
                if user and temp_email and temp_password:
                    full_name = f"{person.first_name} {person.first_last_name}"
                    send_account_created_email(temp_email, full_name, temp_password)
                    email_sent = True
                else:
                    email_error = f"Insufficient data to send email: email={temp_email}, password={temp_password}"
            except Exception as e:
                email_error = str(e)
            if not email_sent:
                print(f"[InstructorService] Could not send registration email to instructor: {email_error}")

            return {
                "person_id": person.id,
                "user_id": user.id,
                "instructor_id": instructor.id,
                "sede_id": sede.id
            }

    def update_instructor(self, instructor_id, person_data, user_data, instructor_data, sede_id):
        """
        Update instructor, user, person, and person_sede. Validate data and roles.
        """
        with transaction.atomic():
            instructor = Instructor.objects.get(pk=instructor_id)
            # Convert the ID to instance if present in instructor_data
            if 'knowledgeArea' in instructor_data:
                knowledge_area_id = instructor_data.pop('knowledgeArea')
                instructor_data['knowledgeArea'] = KnowledgeArea.objects.get(pk=knowledge_area_id)

            # Handle new optional fields
            assigned_learners = instructor_data.pop('assigned_learners', None)
            max_assigned_learners = instructor_data.pop('max_assigned_learners', 80)
            instructor_data['assigned_learners'] = assigned_learners
            instructor_data['max_assigned_learners'] = max_assigned_learners

            # Get the user using the Person object linked to the Instructor
            person = instructor.person
            user = User.objects.filter(person=person).first()

            # Reusable validations for update (excluding the current user)
            if not is_unique_email(user_data['email'], User, exclude_user_id=user.id if user else None):
                raise ValueError('El correo ya está registrado.')
            # Allow the identification number to be the same as the current one
            if int(person_data['number_identification']) != int(person.number_identification):
                if not is_unique_document_number(person_data['number_identification'], Person, exclude_person_id=person.id):
                    raise ValueError('El número de documento ya está registrado.')
            # Phone number validation
            if person_data.get('phone_number') and not is_valid_phone_number(person_data['phone_number']):
                raise ValueError('El número de teléfono debe tener exactamente 10 dígitos.')

            self.repository.update_all_dates_instructor(
                instructor,
                person_data,
                user_data,
                instructor_data,
                sede_id=sede_id
            )
            return {
                "person_id": person.id,
                "user_id": user.id if user else None,
                "instructor_id": instructor.id,
                "sede_id": sede_id
            }

    def delete_instructor(self, instructor_id):
        """
        Completely delete an instructor and related data.
        """
        with transaction.atomic():
            instructor = Instructor.objects.get(pk=instructor_id)
            self.repository.delete_all_dates_instructor(instructor)

    def logical_delete_instructor(self, instructor_id):
        """
        Perform logical deletion or reactivation of instructor.
        """
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
            self.repository.set_active_state_dates_instructor(instructor, active=False)
            return "Eliminación lógica realizada correctamente."


