from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.PersonRepository import PersonRepository
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.UserSerializer import UserSerializer
from apps.security.services.UserService import UserService
from apps.security.emails.SendEmails import enviar_registro_pendiente
from rest_framework import status
from datetime import datetime
from django.contrib.auth.hashers import make_password
from apps.security.entity.models import Person
from apps.security.entity.models import User

class PersonService(BaseService):

    def update(self, pk, data):
        person = self.get(pk)
        return self.update_person(person, data)

    def partial_update(self, pk, data):
        person = self.get(pk)
        return self.update_person(person, data)

    def update_person(self, person, data):
        # Si se va a actualizar la imagen, eliminar la anterior
        if 'image' in data and data['image'] and person.image:
            import os
            if hasattr(person.image, 'path') and os.path.isfile(person.image.path):
                os.remove(person.image.path)
        return self.repository.update_person(person, data)
    def __init__(self):
        super().__init__(PersonRepository())

    def register_aprendiz(self, data):

        email = data.get('email')
        password = data.get('password')
        numero_identificacion = data.get('number_identification')
        # Validar correo institucional
        if not email or not email.endswith('@soy.sena.edu.co'):
            return {
                'data': {'error': 'Solo se permiten correos institucionales'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Validar que el correo institucional no esté repetido en User
        if User.objects.filter(email=email).exists():
            return {
                'data': {'error': 'El correo institucional ya está registrado.'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Validar que el número de identificación no esté repetido en Person
        if Person.objects.filter(number_identification=numero_identificacion).exists():
            return {
                'data': {'error': 'El número de identificación ya está registrado.'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Crear persona usando método base del repositorio
        person, person_data, person_errors = self.repository.create_person(data)
        if not person:
            return {
                'data': {'error': 'Datos inválidos', 'detalle': person_errors},
                'status': status.HTTP_400_BAD_REQUEST
            }
        # Encriptar la contraseña antes de crear el usuario
        hashed_password = make_password(password)
        user_data = {
            'email': email,
            'password': hashed_password,
            'person': person.id,
            'is_active': False,
            'role': 3,  # Rol de Aprendiz
        }
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            # Si falla, eliminar la persona para evitar datos basura
            self.repository.delete_person(person)
            return {
                'data': {'error': 'No se pudo crear el usuario', 'detalle': user_serializer.errors},
                'status': status.HTTP_400_BAD_REQUEST
            }
        user = user_serializer.save()
        
        # Crear Aprendiz vinculado a la persona (ficha se asignará después por el administrador)
        from apps.general.entity.models import Aprendiz
        aprendiz = Aprendiz.objects.create(person=person, ficha=None)
        
        # Si todo es exitoso, enviar correo
        fecha_registro = datetime.now().strftime('%d/%m/%Y')
        enviar_registro_pendiente(email, person.first_name + ' ' + person.first_last_name, fecha_registro)
        return {
            'data': {
                'persona': person_data,
                'usuario': user_serializer.data,
                'aprendiz_id': aprendiz.id,
                'success': 'Usuario registrado correctamente. Tu cuenta está pendiente de activación.'
            },
            'status': status.HTTP_201_CREATED
        }