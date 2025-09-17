from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.PersonRepository import PersonRepository
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.UserSerializer import UserSerializer
from apps.security.services.UserService import UserService
from apps.security.emails.SendEmails import enviar_registro_pendiente
from rest_framework import status
from datetime import datetime
from django.contrib.auth.hashers import make_password
import random
import string

from apps.security.entity.models import Person
from apps.security.entity.models import User
from django.db import transaction

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

    def _generate_temporal_password(self, number_identification):
        """
        Genera una contraseña temporal basada en el número de identificación
        más caracteres especiales aleatorios.
        Formato: [numero_identificacion][2_especiales][2_numeros]
        """
        # Caracteres especiales permitidos
        special_chars = ['!', '@', '#', '$', '%', '&', '*', '+', '=', '?']
        
        # Generar 2 caracteres especiales aleatorios
        random_specials = ''.join(random.choices(special_chars, k=2))
        
        # Generar 2 números aleatorios
        random_numbers = ''.join(random.choices(string.digits, k=2))
        
        # Combinar: número de identificación + especiales + números
        temporal_password = f"{number_identification}{random_specials}{random_numbers}"
        
        return temporal_password

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
        
        # Validar tipo de identificación según enum
        from apps.security.entity.enums.document_type_enum import DocumentType
        valid_types = [doc_type.name for doc_type in DocumentType]
        if type_identification not in valid_types:
            return {
                'data': {'error': f'Tipo de identificación inválido. Opciones válidas: {", ".join(valid_types)}'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        
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
        
        # Generar contraseña temporal basada en el número de documento
        temporal_password = self._generate_temporal_password(numero_identificacion)
        
        try:
            with transaction.atomic():
                # Crear persona usando método base del repositorio
                person, person_data, person_errors = self.repository.create_person(data)
                if not person:
                    raise Exception({'error': 'Datos inválidos', 'detalle': person_errors})
                
                # Encriptar la contraseña antes de crear el usuario
                hashed_password = make_password(temporal_password)
                user_data = {
                    'email': email,
                    'password': hashed_password,
                    'person': person.id,
                    'is_active': False,
                    'role': 2,  # Rol de Aprendiz
                }
                user_serializer = UserSerializer(data=user_data)
                if not user_serializer.is_valid():
                    raise Exception({'error': 'No se pudo crear el usuario', 'detalle': user_serializer.errors})
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
                        'password_temporal': temporal_password,
                        'success': 'Usuario registrado correctamente. Tu cuenta está pendiente de activación.'
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