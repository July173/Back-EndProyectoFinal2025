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
    def delete_custom(self, asignation_instructor_id):
        """
        Deletes an instructor assignment and updates the assigned learners count.
        """
        try:
            from apps.assign.entity.models import AsignationInstructor
            asignation = AsignationInstructor.objects.get(id=asignation_instructor_id)
            instructor = asignation.instructor
            current_learners = instructor.assigned_learners or 0
            from apps.general.services.InstructorService import InstructorService
            InstructorService().update_learners_fields(instructor.id, assigned_learners=max(current_learners - 1, 0))
            asignation.delete()
            return {"status": "success", "message": "Asignación eliminada y contador actualizado."}
        except AsignationInstructor.DoesNotExist:
            return self.error_response("La asignación no existe.", "not_found")  # User-facing error in Spanish
        except Exception as e:
            return self.error_response(f"Error al eliminar la asignación: {e}", "delete_custom")  # User-facing error in Spanish

    def __init__(self):
        self.repository = AsignationInstructorRepository()

    def error_response(self, message, error_type="error"):
        """
        Returns a standardized error response.
        """
        return {"status": "error", "type": error_type, "message": str(message)}

    def create_custom(self, instructor_id, request_asignation_id):
        """
        Creates a custom instructor assignment, updates states, and sends notifications.
        """
        try:
            instructor = Instructor.objects.get(id=instructor_id)
            request_asignation = RequestAsignation.objects.get(id=request_asignation_id)

            # Validate that the state is not REJECTED
            if request_asignation.request_state == RequestState.RECHAZADO:
                return self.error_response("No se puede asignar un instructor a una solicitud rechazada.", "invalid_state")  # User-facing error in Spanish

            # Validate that the instructor has not reached their maximum number of assigned learners
            current_learners = instructor.assigned_learners or 0
            max_learners = instructor.max_assigned_learners or 80

            if current_learners >= max_learners:
                return self.error_response(
                    f"El instructor ha alcanzado su límite máximo de aprendices ({max_learners}). No se pueden asignar más aprendices.",
                    "limit_reached"
                )  # User-facing error in Spanish

            asignation = self.repository.create_custom(instructor, request_asignation)
            request_asignation.request_state = RequestState.ASIGNADO
            request_asignation.save()

            # Update assigned learners for the instructor
            InstructorService().update_learners_fields(instructor_id, assigned_learners=current_learners + 1)

            # Send email to apprentice
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
            # Send email to assigned instructor
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
            return self.error_response("El instructor no existe.", "not_found")  # User-facing error in Spanish
        except RequestAsignation.DoesNotExist:
            return self.error_response("La solicitud de asignación no existe.", "not_found")  # User-facing error in Spanish
        except Exception as e:
            return self.error_response(f"Error al crear la asignación: {e}", "create_custom")  # User-facing error in Spanish

