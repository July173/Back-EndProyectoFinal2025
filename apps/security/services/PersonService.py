from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.PersonRepository import PersonRepository
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.UserSerializer import UserSerializer
from apps.security.services.UserService import UserService
from apps.security.emails.SendEmails import enviar_registro_pendiente
from rest_framework import status
from datetime import datetime
from django.contrib.auth.hashers import make_password
from apps.security.entity.models import Person, User
from django.db import transaction
from apps.security.entity.models.DocumentType import DocumentType
from apps.general.entity.models import Aprendiz


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
        # El serializer ahora maneja correctamente el id, solo delegamos al repositorio
        return self.repository.create_person(data)

    def update_person(self, person, data):
        # Si se va a actualizar la imagen, eliminar la anterior
        if 'image' in data and data['image'] and person.image:
            import os
            if hasattr(person.image, 'path') and os.path.isfile(person.image.path):
                os.remove(person.image.path)
        return self.repository.update_person(person, data)

    def register_aprendiz(self, data):
        """
        Lógica de negocio para registrar un aprendiz.
        Aplica todas las validaciones y reglas de negocio.
        """
        email = data.get('email')
        numero_identificacion = data.get('number_identification')
        type_identification = data.get('type_identification')
        phone_number = data.get('phone_number')

        # === VALIDACIONES DE NEGOCIO ===

        # Validar correo institucional
        if not email or not email.endswith('@soy.sena.edu.co'):
            return {
                'data': {'error': 'Solo se permiten correos institucionales (@soy.sena.edu.co)'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # Validar que el correo no esté repetido
        if User.objects.filter(email=email).exists():
            return {
                'data': {'error': 'El correo institucional ya está registrado.'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # Validar que el número de identificación no esté repetido
        if Person.objects.filter(number_identification=numero_identificacion).exists():
            return {
                'data': {'error': 'El número de identificación ya está registrado.'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # Nota: La validación del tipo de identificación se hace en PersonSerializer
        # El serializer ya valida que el ID exista y esté activo

        # Validar número de identificación
        if not numero_identificacion or len(str(numero_identificacion).strip()) < 6:
            return {
                'data': {'error': 'El número de identificación debe tener al menos 6 dígitos'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # Validar teléfono
        if not phone_number or len(str(phone_number)) < 10:
            return {
                'data': {'error': 'El número de teléfono debe tener al menos 10 dígitos'},
                'status': status.HTTP_400_BAD_REQUEST
            }

        # === LÓGICA DE NEGOCIO ===

        try:
            with transaction.atomic():
                # Crear persona usando el método del service que transforma el id
                person, person_data, person_errors = self.create_person(data)
                if not person:
                    raise Exception({'error': 'Datos inválidos', 'detalle': person_errors})

                # Crear usuario inactivo sin contraseña (se establecerá cuando se active)
                user_data = {
                    'email': email,
                    'password': make_password('temporal_placeholder'),  # Contraseña temporal que será reemplazada
                    'person': person.id,
                    'is_active': False,
                    'role': 2,  # Rol de Aprendiz
                }
                user_serializer = UserSerializer(data=user_data)
                if not user_serializer.is_valid():
                    raise Exception({'error': 'No se pudo crear el usuario', 'detalle': user_serializer.errors})
                user = user_serializer.save()

                # Crear Aprendiz vinculado a la persona (ficha se asignará después por el administrador)
                aprendiz = Aprendiz.objects.create(person=person, ficha=None)

                # Si todo es exitoso, enviar correo de registro pendiente
                fecha_registro = datetime.now().strftime('%d/%m/%Y')
                enviar_registro_pendiente(email, person.first_name + ' ' + person.first_last_name, fecha_registro)

                return {
                    'data': {
                        'persona': person_data,
                        'usuario': user_serializer.data,
                        'aprendiz_id': aprendiz.id,
                        'success': 'Usuario registrado correctamente. Tu cuenta está pendiente de activación por un administrador.'
                    },
                    'status': status.HTTP_201_CREATED
                }
        except Exception as e:
            # Si ocurre cualquier error, se hace rollback automáticamente
            detalle = str(e)
            # Si el error es un diccionario, extraer el mensaje
            if hasattr(e, 'args') and len(e.args) > 0 and isinstance(e.args[0], dict):
                detalle = e.args[0]
            return {
                'data': {'error': 'No se pudo completar el registro', 'detalle': detalle},
                'status': status.HTTP_400_BAD_REQUEST
            }