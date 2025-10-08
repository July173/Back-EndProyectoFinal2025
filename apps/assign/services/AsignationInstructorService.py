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
    def delete_custom(self, asignation_instructor_id):
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
            return self.error_response("La asignación no existe.", "not_found")
        except Exception as e:
            return self.error_response(f"Error al eliminar la asignación: {e}", "delete_custom")
    def __init__(self):
        self.repository = AsignationInstructorRepository()

    def error_response(self, message, error_type="error"):
        return {"status": "error", "type": error_type, "message": str(message)}

    def create_custom(self, instructor_id, request_asignation_id):
        try:
            instructor = Instructor.objects.get(id=instructor_id)
            request_asignation = RequestAsignation.objects.get(id=request_asignation_id)
            
            # Validar que el estado no sea RECHAZADO
            if request_asignation.request_state == RequestState.RECHAZADO:
                return self.error_response("No se puede asignar un instructor a una solicitud rechazada.", "invalid_state")
            
            # Validar que el instructor no haya alcanzado su límite máximo de aprendices
            current_learners = instructor.assigned_learners or 0
            max_learners = instructor.max_assigned_learners or 80
            
            if current_learners >= max_learners:
                return self.error_response(
                    f"El instructor ha alcanzado su límite máximo de aprendices ({max_learners}). No se pueden asignar más aprendices.",
                    "limit_reached"
                )
            
            asignation = self.repository.create_custom(instructor, request_asignation)
            request_asignation.request_state = RequestState.ASIGNADO
            request_asignation.save()
            
            # Actualizar aprendices asignados al instructor
            InstructorService().update_learners_fields(instructor_id, assigned_learners=current_learners + 1)
            
            # Enviar correo al aprendiz
            aprendiz = request_asignation.aprendiz
            person = aprendiz.person
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
            # Enviar correo al instructor asignado
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
            return self.error_response("El instructor no existe.", "not_found")
        except RequestAsignation.DoesNotExist:
            return self.error_response("La solicitud de asignación no existe.", "not_found")
        except Exception as e:
            return self.error_response(f"Error al crear la asignación: {e}", "create_custom")

