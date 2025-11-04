from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.InstructorRepository import InstructorRepository
from django.db import transaction
from apps.general.entity.models import Sede, KnowledgeArea
from apps.security.entity.models import User, Person
from apps.general.entity.models import Instructor
from apps.security.emails.CreacionCuentaUsers import send_account_created_email
from core.utils.Validation import is_unique_email, validate_document_number, validate_phone_number
from django.utils.crypto import get_random_string
from core.utils.Validation import is_sena_email
from django.core.exceptions import ObjectDoesNotExist

class InstructorService(BaseService):
    def update_learners_fields(self, instructor_id, assigned_learners=None, max_assigned_learners=None):
        instructor = Instructor.objects.filter(pk=instructor_id).first()
        if not instructor:
            return None
        # Validación: assigned_learners nunca menor que 0
        if assigned_learners is not None:
            if assigned_learners < 0:
                raise ValueError('El número de aprendices asignados no puede ser menor que 0.')
            # Validación: no superar el límite
            max_limit = max_assigned_learners if max_assigned_learners is not None else instructor.max_assigned_learners or 80
            if assigned_learners > max_limit:
                raise ValueError('El número de aprendices asignados no puede superar el límite máximo.')
            instructor.assigned_learners = assigned_learners
        if max_assigned_learners is not None:
            if max_assigned_learners < 0:
                raise ValueError('El límite máximo no puede ser menor que 0.')
            instructor.max_assigned_learners = max_assigned_learners
            # Si el límite se reduce por debajo de los asignados, ajusta los asignados
            if instructor.assigned_learners is not None and instructor.assigned_learners > max_assigned_learners:
                instructor.assigned_learners = max_assigned_learners
        instructor.save()
        return instructor

    def __init__(self):
        self.repository = InstructorRepository()

    def list_instructors(self):
        """
        Devuelve todos los instructores.
        """
        return Instructor.objects.all()

    def create_instructor(self, person_data, user_data, instructor_data, sede_id):
        with transaction.atomic():
            # Obtener la sede y sus relaciones
            try:
                sede = Sede.objects.get(id=sede_id)
            except ObjectDoesNotExist:
                raise ValueError(f'La sede con id {sede_id} no existe.')

            # Preparar datos para KnowledgeArea
            knowledge_area_id = instructor_data.pop('knowledgeArea')
            knowledge_area_instance = KnowledgeArea.objects.get(pk=knowledge_area_id)
            instructor_data['knowledgeArea'] = knowledge_area_instance

            # Manejar nuevos campos opcionales
            assigned_learners = instructor_data.pop('assigned_learners', None)
            max_assigned_learners = instructor_data.pop('max_assigned_learners', 80)
            instructor_data['assigned_learners'] = assigned_learners
            instructor_data['max_assigned_learners'] = max_assigned_learners

            # Preparar datos para user
            numero_identificacion = str(person_data['number_identification'])
            caracteres_adicionales = get_random_string(length=2)
            password_temporal = numero_identificacion + caracteres_adicionales
            user_data['password'] = password_temporal
            temp_email = user_data.get('email')
            temp_password = password_temporal

            # Validación de correo institucional @sena.edu.co
            if not temp_email or not is_sena_email(temp_email):
                raise ValueError('Solo se permiten correos institucionales (@sena.edu.co) para instructores.')

            # Validaciones reutilizables
            if not is_unique_email(user_data['email'], User):
                raise ValueError('El correo ya está registrado.')
            if not validate_document_number(person_data['number_identification'], Person):
                raise ValueError('El número de documento ya está registrado.')
            if person_data.get('phone_number') and not validate_phone_number(person_data['phone_number']):
                raise ValueError('El número de teléfono debe tener exactamente 10 dígitos.')

            # Crear todo en una sola transacción
            instructor, user, person, person_sede = self.repository.create_all_dates_instructor(
                person_data, user_data, instructor_data, sede_id=sede.id
            )

            # Validar datos antes de enviar el correo
            email_sent = False
            email_error = None
            try:
                if user and temp_email and temp_password:
                    full_name = f"{person.first_name} {person.first_last_name}"
                    send_account_created_email(temp_email, full_name, temp_password)
                    email_sent = True
                else:
                    email_error = f"Datos insuficientes para enviar correo: email={temp_email}, password={temp_password}"
            except Exception as e:
                email_error = str(e)
            if not email_sent:
                print(f"[InstructorService] No se pudo enviar el correo de registro al instructor: {email_error}")

            return {
                "person_id": person.id,
                "user_id": user.id,
                "instructor_id": instructor.id,
                "sede_id": sede.id
            }

    def update_instructor(self, instructor_id, person_data, user_data, instructor_data, sede_id):
        with transaction.atomic():
            instructor = Instructor.objects.get(pk=instructor_id)
            # Convierte el ID en instancia si existe en instructor_data
            if 'knowledgeArea' in instructor_data:
                knowledge_area_id = instructor_data.pop('knowledgeArea')
                instructor_data['knowledgeArea'] = KnowledgeArea.objects.get(pk=knowledge_area_id)

            # Manejar nuevos campos opcionales
            assigned_learners = instructor_data.pop('assigned_learners', None)
            max_assigned_learners = instructor_data.pop('max_assigned_learners', 80)
            instructor_data['assigned_learners'] = assigned_learners
            instructor_data['max_assigned_learners'] = max_assigned_learners

            # Obtener el usuario usando el objeto Person vinculado al Instructor
            person = instructor.person
            user = User.objects.filter(person=person).first()

            # Validaciones reutilizables para update (excluyendo el usuario actual)
            if not is_unique_email(user_data['email'], User, exclude_user_id=user.id if user else None):
                raise ValueError('El correo ya está registrado.')
            # Permitir que el número de identificación sea el mismo que el actual
            if int(person_data['number_identification']) != int(person.number_identification):
                if not validate_document_number(person_data['number_identification'], Person, exclude_person_id=person.id):
                    raise ValueError('El número de documento ya está registrado.')
            # Validación de número de teléfono
            if person_data.get('phone_number') and not validate_phone_number(person_data['phone_number']):
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
