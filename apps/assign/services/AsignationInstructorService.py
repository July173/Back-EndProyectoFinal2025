from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.AsignationInstructorRepository import AsignationInstructorRepository
from apps.general.entity.models import Instructor
from apps.assign.entity.models import RequestAsignation
from apps.assign.entity.enums.request_state_enum import RequestState
from apps.security.entity.models import User
from apps.security.emails.AsignacionInstructor import send_instructor_assignment_email
from apps.security.emails.AsignacionInstructor import send_assignment_to_instructor_email
from apps.general.services.InstructorService import InstructorService

class AsignationInstructorService(BaseService):
    """
    Service for managing instructor assignments and related logic.
    """

    def __init__(self):
        self.repository = AsignationInstructorRepository()

    def create(self, validated_data):
        """
        Creates an instructor assignment, updates states, and sends notifications.
        """
        try:
            instructor_id = validated_data.get('instructor')
            request_asignation_id = validated_data.get('request_asignation')
            instructor = Instructor.objects.get(id=instructor_id)
            request_asignation = RequestAsignation.objects.get(id=request_asignation_id)

            # Validate that the request is not rejected
            if request_asignation.request_state == RequestState.RECHAZADO:
                raise Exception("No se puede asignar un instructor a una solicitud rechazada.")

            # Validate that the instructor has not reached the maximum number of learners
            current_learners = instructor.assigned_learners or 0
            max_learners = instructor.max_assigned_learners or 80
            if current_learners >= max_learners:
                raise Exception(f"El instructor ha alcanzado su límite máximo de aprendices ({max_learners}). No se pueden asignar más aprendices.")

            asignation = self.repository.create_custom(instructor, request_asignation)
            request_asignation.request_state = RequestState.ASIGNADO
            request_asignation.save()

            # Update assigned learners for the instructor
            InstructorService().update_learners_fields(instructor_id, assigned_learners=current_learners + 1)

            # Send email to the apprentice
            apprentice = request_asignation.apprentice
            person = apprentice.person
            user = User.objects.filter(person=person).first()
            email = user.email if user else None
            if email:
                send_instructor_assignment_email(
                    email,
                    f"{person.first_name} {person.first_last_name}",
                    f"{instructor.person.first_name} {instructor.person.first_last_name}",
                    person.number_identification,
                    email
                )
            # Send email to the assigned instructor
            instructor_user = User.objects.filter(person=instructor.person).first()
            instructor_email = instructor_user.email if instructor_user else None
            if instructor_email:
                send_assignment_to_instructor_email(
                    instructor_email,
                    f"{person.first_name} {person.first_last_name}",
                    f"{instructor.person.first_name} {instructor.person.first_last_name}"
                )
            return asignation
        except Instructor.DoesNotExist:
            raise Exception("El instructor no existe.")
        except RequestAsignation.DoesNotExist:
            raise Exception("La solicitud de asignación no existe.")
        except Exception as e:
            raise Exception(f"Error al crear la asignación: {e}")

