from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.ApprenticeRepository import ApprenticeRepository
from apps.security.entity.models import User, Role, Person
from apps.general.entity.models import Apprentice, Ficha
from apps.security.emails.CreacionCuentaUsers import send_account_created_email
from django.db import transaction
from django.db import models
from core.utils.Validation import is_unique_email, is_unique_document_number, is_valid_phone_number
from apps.security.entity.models.DocumentType import DocumentType
from django.utils.crypto import get_random_string
from core.utils.Validation import is_soy_sena_email


class ApprenticeService(BaseService):
    """
    Service for managing apprentice creation, update, deletion, and activation logic.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """

    def __init__(self):
        self.repository = ApprenticeRepository()

    def create_apprentice(self, validated_data):
        """
        Create an apprentice, user, and person. Validate data and send welcome email.
        """
        # Validate document type from the database
        type_identification = validated_data['type_identification']

        # Check that the document type exists and is active in the database
        if isinstance(type_identification, int):
            # If it comes as an ID, check existence
            if not DocumentType.objects.filter(pk=type_identification, active=True).exists():
                valid_types = DocumentType.objects.filter(active=True).values_list('id', 'name')
                valid_types_str = ', '.join([f"{id}: {name}" for id, name in valid_types])
                raise ValueError(f'Invalid identification type. Valid options: {valid_types_str}')
        else:
            # If it comes as a string (acronym or name), look up the ID
            doc_type = DocumentType.objects.filter(
                models.Q(acronyms=type_identification) | models.Q(name=type_identification),
                active=True
            ).first()
            if not doc_type:
                valid_types = DocumentType.objects.filter(active=True).values_list('acronyms', 'name')
                valid_types_str = ', '.join([f"{acronym} ({name})" for acronym, name in valid_types])
                raise ValueError(f'Invalid identification type. Valid options: {valid_types_str}')
            # Replace with the ID for later use
            type_identification = doc_type.id
            validated_data['type_identification'] = doc_type.id

        # Build person data
        person_data = {
            'type_identification_id': type_identification,  # Use _id for ForeignKey field
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        # Build user data
        user_data = {
            'email': validated_data['email'],
            'person_id': None  # Assigned in the repository
        }
        ficha_id = validated_data['ficha_id']

        # Institutional email validation
        if not user_data['email'] or not is_soy_sena_email(user_data['email']):
            raise ValueError('Only institutional emails (@soy.sena.edu.co) are allowed for apprentices.')

        # Uniqueness and format validations
        if not is_unique_email(user_data['email'], User):
            raise ValueError('Email is already registered.')
        if not is_unique_document_number(person_data['number_identification'], Person):
            raise ValueError('Document number is already registered.')
        if person_data['phone_number'] and not is_valid_phone_number(person_data['phone_number']):
            raise ValueError('Phone number must be exactly 10 digits.')

        with transaction.atomic():
            # Assign password as document number + 2 random characters
            numero_identificacion = str(person_data['number_identification'])
            caracteres_adicionales = get_random_string(length=2)
            password_temporal = numero_identificacion + caracteres_adicionales
            user_data['password'] = password_temporal
            if not user_data.get('role_id'):
                try:
                    default_role = Role.objects.get(pk=2)
                    user_data['role_id'] = default_role.id
                except Role.DoesNotExist:
                    pass

            # Get ficha and create records
            email = user_data.get('email')
            temp_password = password_temporal
            ficha = Ficha.objects.get(pk=ficha_id)
            aprendiz, user, person = self.repository.create_all_dates_apprentice(person_data, user_data, ficha)

            # Send welcome email
            email_sent = False
            email_error = None
            try:
                if user and email and temp_password:
                    full_name = f"{person_data.get('first_name', '')} {person_data.get('first_last_name', '')}"
                    send_account_created_email(email, full_name, temp_password)
                    email_sent = True
                else:
                    email_error = f"Insufficient data to send email: email={email}, password={temp_password}"
            except Exception as e:
                email_error = str(e)
            if not email_sent:
                print(f"[ApprenticeService] Could not send registration email to apprentice: {email_error}")
            return aprendiz, user, person

    def update_apprentice(self, aprendiz_id, validated_data):
        """
        Update apprentice, user, and person data. Validate data and roles.
        """
        # Validate and get the document type ID
        type_identification = validated_data.get('type_identification')
        if type_identification:
            if isinstance(type_identification, int):
                # If it comes as an ID, check existence
                if not DocumentType.objects.filter(pk=type_identification, active=True).exists():
                    raise ValueError('Invalid identification type')
            else:
                # If it comes as a string (acronym or name), look up the ID
                doc_type = DocumentType.objects.filter(
                    models.Q(acronyms=type_identification) | models.Q(name=type_identification),
                    active=True
                ).first()
                if not doc_type:
                    raise ValueError('Invalid identification type')
                type_identification = doc_type.id

        # Build person data
        person_data = {
            'type_identification_id': type_identification,  # Use _id for ForeignKey field
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        # Build user data
        user_data = {
            'email': validated_data['email'],
        }
        ficha_id = validated_data['ficha_id']
        role_id = validated_data['role_id']

        apprentice = Apprentice.objects.get(pk=aprendiz_id)
        # Institutional email validation
        if not user_data['email'] or not is_soy_sena_email(user_data['email']):
            raise ValueError('Only institutional emails (@soy.sena.edu.co) are allowed for apprentices.')
        # Get the user using the relation to person
        user = User.objects.filter(person=apprentice.person).first()
        # Uniqueness and format validations
        if not is_unique_email(user_data['email'], User, exclude_user_id=user.id if user else None):
            raise ValueError('Email is already registered.')
        if not is_unique_document_number(person_data['number_identification'], Person, exclude_person_id=apprentice.person.id):
            raise ValueError('Document number is already registered.')
        if person_data['phone_number'] and not is_valid_phone_number(person_data['phone_number']):
            raise ValueError('Phone number must be exactly 10 digits.')

        with transaction.atomic():
            # Update ficha and role
            aprendiz = Apprentice.objects.get(pk=aprendiz_id)
            ficha = Ficha.objects.get(pk=ficha_id)
            if not role_id:
                role_id = 2
            try:
                role = Role.objects.get(pk=role_id)
                user_data['role_id'] = role.id
            except Role.DoesNotExist:
                user_data['role_id'] = 2
            self.repository.update_all_dates_apprentice(aprendiz, person_data, user_data, ficha)
            return apprentice

    def get_aprendiz(self, aprendiz_id):
        """
        Get an apprentice by ID.
        """
        return Apprentice.objects.filter(pk=aprendiz_id).first()

    def list_aprendices(self):
        """
        List all apprentices.
        """
        return Apprentice.objects.all()

    def delete_aprendiz(self, aprendiz_id):
        """
        Completely delete an apprentice and related data.
        """
        with transaction.atomic():
            aprendiz = Apprentice.objects.get(pk=aprendiz_id)
            self.repository.delete_all_dates_apprentice(aprendiz)

    def logical_delete_aprendiz(self, aprendiz_id):
        """
        Perform logical deletion or reactivation of apprentice.
        """
        with transaction.atomic():
            aprendiz = Apprentice.objects.get(pk=aprendiz_id)
            if not aprendiz.active:
                self.repository.set_active_state_dates_apprentice(aprendiz, active=True)
                return "Aprendiz reactivado correctamente."
            else:
                self.repository.set_active_state_dates_apprentice(aprendiz, active=False)
                return "Eliminación lógica realizada correctamente."


