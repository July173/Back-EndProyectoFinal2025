from apps.assign.repositories.AsignationInstructorHistoryRepository import AsignationInstructorHistoryRepository
from apps.assign.entity.models import AsignationInstructor
from apps.general.entity.models import Instructor
from apps.security.entity.models import User
from apps.assign.emails.DesvinculacionInstructor import send_unassignment_to_instructor_email
from apps.assign.emails.ReasignacionInstructor import send_assignment_to_new_instructor_email
from apps.assign.emails.DesvinculacionAprendiz import send_unassignment_to_aprendiz_email


class AsignationInstructorHistoryService:
    """
    Service for managing instructor assignment history and reassignments.
    """
    def __init__(self):
        self.repository = AsignationInstructorHistoryRepository()

    def error_response(self, message, error_type="error"):
        """
        Returns a standardized error response.
        """
        return {"status": "error", "type": error_type, "message": str(message)}

    def list_by_asignation(self, asignation_instructor_id):
        """
        Lists the assignment history for a given instructor assignment.
        """
        try:
            return self.repository.list_by_asignation(asignation_instructor_id)
        except Exception as e:
            return self.error_response(f"No se pudo obtener el historial: {e}", "list_by_asignation")  # User-facing error in Spanish

    def reasignar_instructor(self, asignation_instructor_id, new_instructor_id, message):
        """
        Reassigns an instructor to a new one, updates history, and sends notifications.
        """
        try:
            asignation_instructor = AsignationInstructor.objects.get(id=asignation_instructor_id)
            old_instructor = asignation_instructor.instructor
            old_instructor_id = old_instructor.id
            new_instructor = Instructor.objects.get(id=new_instructor_id)
            # Save history before updating
            self.repository.create_history(
                asignation_instructor=asignation_instructor,
                old_instructor_id=old_instructor_id,
                message=message
            )
            # Send email to previous instructor
            old_person = old_instructor.person
            old_user = User.objects.filter(person=old_person).first()
            old_email = old_user.email if old_user else None
            nombre_instructor = f"{old_person.first_name} {old_person.first_last_name}"
            aprendiz_person = asignation_instructor.request_asignation.aprendiz.person
            nombre_aprendiz = f"{aprendiz_person.first_name} {aprendiz_person.first_last_name}"
            if old_email:
                send_unassignment_to_instructor_email(old_email, nombre_instructor, nombre_aprendiz)
                # Decrement assigned learners for previous instructor
                from apps.general.services.InstructorService import InstructorService
                current_learners_old = old_instructor.assigned_learners or 0
                InstructorService().update_learners_fields(old_instructor_id, assigned_learners=max(current_learners_old - 1, 0))
            # Send email to new instructor
            new_person = new_instructor.person
            new_user = User.objects.filter(person=new_person).first()
            new_email = new_user.email if new_user else None
            new_instructor_name = f"{new_person.first_name} {new_person.first_last_name}"
            if new_email:
                send_assignment_to_new_instructor_email(new_email, new_instructor_name, nombre_aprendiz)
                # Increment assigned learners for new instructor
                current_learners_new = new_instructor.assigned_learners or 0
                InstructorService().update_learners_fields(new_instructor_id, assigned_learners=current_learners_new + 1)
            # Send email to apprentice
            aprendiz_user = User.objects.filter(person=aprendiz_person).first()
            aprendiz_email = aprendiz_user.email if aprendiz_user else None
            if aprendiz_email:
                send_unassignment_to_aprendiz_email(aprendiz_email, nombre_aprendiz)
            # Update assignment with new instructor
            asignation_instructor.instructor = new_instructor
            asignation_instructor.save()
            return asignation_instructor
        except AsignationInstructor.DoesNotExist:
            return self.error_response("La asignación de instructor no existe.", "not_found")  # User-facing error in Spanish
        except Instructor.DoesNotExist:
            return self.error_response("El nuevo instructor no existe.", "not_found")  # User-facing error in Spanish
        except Exception as e:
            return self.error_response(f"Error al reasignar instructor: {e}", "reasignar_instructor")  # User-facing error in Spanish
