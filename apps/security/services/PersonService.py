from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.PersonRepository import PersonRepository
from apps.security.entity.serializers.User.UserSerializer import UserSerializer
from apps.security.emails.SendEmails import enviar_registro_pendiente
from rest_framework import status
from datetime import datetime
from django.contrib.auth.hashers import make_password
from apps.security.entity.models import Person, User
from django.db import transaction
from apps.general.entity.models import Apprentice
from apps.security.entity.models import Role
from apps.security.entity.serializers.User.UserSerializer import UserSerializer


class PersonService(BaseService):
    def __init__(self):
        super().__init__(PersonRepository())

    def update(self, pk, data):
        person = self.get(pk)
        if not person:
            raise ValueError(f"No se encontró la persona con ID {pk}.")
        try:
            return self.update_person(person, data)
        except Exception as e:
            raise ValueError(f"No se pudo actualizar la persona: {str(e)}")

    def partial_update(self, pk, data):
        person = self.get(pk)
        if not person:
            raise ValueError(f"No se encontró la persona con ID {pk}.")
        try:
            return self.update_person(person, data)
        except Exception as e:
            raise ValueError(f"No se pudo actualizar parcialmente la persona: {str(e)}")

    def create_person(self, data):
        try:
            return self.repository.create_person(data)
        except Exception as e:
            raise ValueError(f"No se pudo crear la persona: {str(e)}")

    def update_person(self, person, data):
        # If the image is being updated, delete the previous one
        try:
            if 'image' in data and data['image'] and person.image:
                import os
                if hasattr(person.image, 'path') and os.path.isfile(person.image.path):
                    os.remove(person.image.path)
            return self.repository.update_person(person, data)
        except Exception as e:
            raise ValueError(f"No se pudo actualizar la persona: {str(e)}")

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

                # Obtener instancia de rol Aprendiz
                rol_apprentice = Role.objects.get(id=2)  # O usa type_role="Aprendiz" si prefieres

                # Crear usuario correctamente vinculado
                user = User.objects.create(
                    email=email,
                    password=make_password('temporal_placeholder'),
                    person=person,
                    is_active=False,
                    role=rol_apprentice,
                )

                # Create Apprentice linked to the person (ficha will be assigned later by admin)
                apprentice = Apprentice.objects.create(person=person, ficha=None)

                # If everything is successful, send pending registration email
                registration_date = datetime.now().strftime('%d/%m/%Y')
                enviar_registro_pendiente(email, person.first_name + ' ' + person.first_last_name, registration_date)

                # Serializar usuario para la respuesta
                user_serializer = UserSerializer(user)

                return {
                    'data': {
                        'persona': person_data,
                        'usuario': user_serializer.data,
                        'apprentice_id': apprentice.id,
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