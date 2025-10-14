from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.PersonRepository import PersonRepository
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.User.UserSerializer import UserSerializer
from apps.security.services.UserService import UserService
from apps.security.emails.SendEmails import enviar_registro_pendiente
from rest_framework import status
from datetime import datetime
from django.contrib.auth.hashers import make_password
from apps.security.entity.models import Person, User
from django.db import transaction
from apps.security.entity.models.DocumentType import DocumentType
from apps.general.entity.models import Apprentice



class PersonService(BaseService):
    def __init__(self):
        super().__init__(PersonRepository())

    def update(self, pk, data):
        person = self.get(pk)
        return self.update_person(person, data)

    def partial_update(self, pk, data):
        person = self.get(pk)
        return self.update_person(person, data)

    def create_person(self, data):
        # The serializer now correctly handles the id, just delegate to the repository
        return self.repository.create_person(data)

    def update_person(self, person, data):
        # If the image is being updated, delete the previous one
        if 'image' in data and data['image'] and person.image:
            import os
            if hasattr(person.image, 'path') and os.path.isfile(person.image.path):
                os.remove(person.image.path)
        return self.repository.update_person(person, data)

    def register_apprentice(self, data):
        """
        Business logic for registering an apprentice.
        Applies all validations and business rules.
        """
        email = data.get('email')
        identification_number = data.get('number_identification')
        identification_type = data.get('type_identification')
        phone_number = data.get('phone_number')

        # === BUSINESS VALIDATIONS ===

        # Validate institutional email
        if not email or not email.endswith('@soy.sena.edu.co'):
            return {
                'data': {'error': 'Solo se permiten correos institucionales (@soy.sena.edu.co)'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # Validate email is not duplicated
        if User.objects.filter(email=email).exists():
            return {
                'data': {'error': 'El correo institucional ya está registrado.'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # Validate identification number is not duplicated
        if Person.objects.filter(number_identification=identification_number).exists():
            return {
                'data': {'error': 'El número de identificación ya está registrado.'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # Note: Identification type validation is handled in PersonSerializer
        # The serializer already validates that the ID exists and is active

        # Validate identification number
        if not identification_number or len(str(identification_number).strip()) < 6:
            return {
                'data': {'error': 'El número de identificación debe tener al menos 6 dígitos'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # Validate phone number
        if not phone_number or len(str(phone_number)) < 10:
            return {
                'data': {'error': 'El número de teléfono debe tener al menos 10 dígitos'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # === BUSINESS LOGIC ===

        try:
            with transaction.atomic():
                # Create person using the service method that transforms the id
                person, person_data, person_errors = self.create_person(data)
                if not person:
                    raise Exception({'error': 'Datos inválidos', 'detalle': person_errors})

                # Create inactive user without password (will be set when activated)
                user_data = {
                    'email': email,
                    'password': make_password('temporal_placeholder'),  # Temporary password to be replaced
                    'person': person.id,
                    'is_active': False,
                    'role': 2,  # Apprentice role
                }
                user_serializer = UserSerializer(data=user_data)
                if not user_serializer.is_valid():
                    raise Exception({'error': 'No se pudo crear el usuario', 'detalle': user_serializer.errors})
                user = user_serializer.save()

                # Create Apprentice linked to the person (ficha will be assigned later by admin)
                apprentice = Apprentice.objects.create(person=person, ficha=None)

                # If everything is successful, send pending registration email
                registration_date = datetime.now().strftime('%d/%m/%Y')
                enviar_registro_pendiente(email, person.first_name + ' ' + person.first_last_name, registration_date)

                return {
                    'data': {
                        'persona': person_data,
                        'usuario': user_serializer.data,
                        'aprendiz_id': apprentice.id,
                        'success': 'Usuario registrado correctamente. Tu cuenta está pendiente de activación por un administrador.'
                    },
                    'status': status.HTTP_201_CREATED
                }
        except Exception as e:
            # If any error occurs, rollback is automatic
            detail = str(e)
            # If the error is a dictionary, extract the message
            if hasattr(e, 'args') and len(e.args) > 0 and isinstance(e.args[0], dict):
                detail = e.args[0]
            return {
                'data': {'error': 'No se pudo completar el registro', 'detalle': detail},
                'status': status.HTTP_400_BAD_REQUEST
            }