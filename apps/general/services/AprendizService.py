from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.AprendizRepository import AprendizRepository
from apps.security.entity.models import User, Role, Person
from apps.general.entity.models import Apprentice, Ficha
from apps.security.emails.CreacionCuentaUsers import send_account_created_email
from django.db import transaction
from django.db import models
from core.utils.Validation import is_unique_email, validate_document_number, validate_phone_number
from apps.security.entity.models.DocumentType import DocumentType
from django.utils.crypto import get_random_string
from core.utils.Validation import is_soy_sena_email


class AprendizService(BaseService):

    def __init__(self):
        self.repository = AprendizRepository()

    def create_aprendiz(self, validated_data):
        """
        Crea un aprendiz, usuario y persona. Valida datos y envía correo de bienvenida.
        """
        # Validar tipo de documento desde la BD
        type_identification = validated_data['type_identification']
        
        # Verificar que el tipo de documento exista y esté activo en la BD
        if isinstance(type_identification, int):
            # Si viene como ID, verificar que exista
            if not DocumentType.objects.filter(pk=type_identification, active=True).exists():
                valid_types = DocumentType.objects.filter(active=True).values_list('id', 'name')
                valid_types_str = ', '.join([f"{id}: {name}" for id, name in valid_types])
                raise ValueError(f'Tipo de identificación inválido. Opciones válidas: {valid_types_str}')
        else:
            # Si viene como string (acronym o name), buscar el ID
            doc_type = DocumentType.objects.filter(
                models.Q(acronyms=type_identification) | models.Q(name=type_identification),
                active=True
            ).first()
            if not doc_type:
                valid_types = DocumentType.objects.filter(active=True).values_list('acronyms', 'name')
                valid_types_str = ', '.join([f"{acronym} ({name})" for acronym, name in valid_types])
                raise ValueError(f'Tipo de identificación inválido. Opciones válidas: {valid_types_str}')
            # Reemplazar con el ID para usarlo después
            type_identification = doc_type.id
            validated_data['type_identification'] = doc_type.id
        
        # Construcción de datos de persona
        person_data = {
            'type_identification_id': type_identification,  # Usar _id para el campo ForeignKey
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        # Construcción de datos de usuario
        user_data = {
            'email': validated_data['email'],
            'person_id': None  # Se asigna en el repo
        }
        ficha_id = validated_data['ficha_id']

        # Validación de correo institucional
        if not user_data['email'] or not is_soy_sena_email(user_data['email']):
            raise ValueError('Solo se permiten correos institucionales (@soy.sena.edu.co) para aprendices.')

        # Validaciones de unicidad y formato
        if not is_unique_email(user_data['email'], User):
            raise ValueError('El correo ya está registrado.')
        if not validate_document_number(person_data['number_identification'], Person):
            raise ValueError('El número de documento ya está registrado.')
        if person_data['phone_number'] and not validate_phone_number(person_data['phone_number']):
            raise ValueError('El número de teléfono debe tener exactamente 10 dígitos.')

        with transaction.atomic():
            # Asigna la contraseña como número de documento + 2 caracteres aleatorios
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

            # Obtiene ficha y crea registros
            email = user_data.get('email')
            temp_password = password_temporal
            ficha = Ficha.objects.get(pk=ficha_id)
            aprendiz, user, person = self.repository.create_all_dates_apprentice(person_data, user_data, ficha)

            # Envía correo de bienvenida
            email_sent = False
            email_error = None
            try:
                if user and email and temp_password:
                    full_name = f"{person_data.get('first_name', '')} {person_data.get('first_last_name', '')}"
                    send_account_created_email(email, full_name, temp_password)
                    email_sent = True
                else:
                    email_error = f"Datos insuficientes para enviar correo: email={email}, password={temp_password}"
            except Exception as e:
                email_error = str(e)
            if not email_sent:
                print(f"[AprendizService] No se pudo enviar el correo de registro al aprendiz: {email_error}")
            return aprendiz, user, person

    def update_aprendiz(self, aprendiz_id, validated_data):
        """
        Actualiza los datos de aprendiz, usuario y persona. Valida datos y roles.
        """
        
        # Validar y obtener el ID del tipo de documento
        type_identification = validated_data.get('type_identification')
        if type_identification:
            if isinstance(type_identification, int):
                # Si viene como ID, verificar que exista
                if not DocumentType.objects.filter(pk=type_identification, active=True).exists():
                    raise ValueError('Tipo de identificación inválido')
            else:
                # Si viene como string (acronym o name), buscar el ID
                doc_type = DocumentType.objects.filter(
                    models.Q(acronyms=type_identification) | models.Q(name=type_identification),
                    active=True
                ).first()
                if not doc_type:
                    raise ValueError('Tipo de identificación inválido')
                type_identification = doc_type.id
        
        # Construcción de datos de persona
        person_data = {
            'type_identification_id': type_identification,  # Usar _id para el campo ForeignKey
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        # Construcción de datos de usuario
        user_data = {
            'email': validated_data['email'],
        }
        ficha_id = validated_data['ficha_id']
        role_id = validated_data['role_id']

        aprendiz = Apprentice.objects.get(pk=aprendiz_id)
        # Validación de correo institucional
        if not user_data['email'] or not is_soy_sena_email(user_data['email']):
            raise ValueError('Solo se permiten correos institucionales (@soy.sena.edu.co) para aprendices.')
        # Obtener el usuario usando la relación con la persona
        user = User.objects.filter(person=aprendiz.person).first()
        # Validaciones de unicidad y formato
        if not is_unique_email(user_data['email'], User, exclude_user_id=user.id if user else None):
            raise ValueError('El correo ya está registrado.')
        if not validate_document_number(person_data['number_identification'], Person, exclude_person_id=aprendiz.person.id):
            raise ValueError('El número de documento ya está registrado.')
        if person_data['phone_number'] and not validate_phone_number(person_data['phone_number']):
            raise ValueError('El número de teléfono debe tener exactamente 10 dígitos.')

        with transaction.atomic():
            # Actualiza ficha y rol
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
            return aprendiz
    
    def list_aprendices(self):
        """
        Lista todos los aprendices.
        """
        return Apprentice.objects.all()
