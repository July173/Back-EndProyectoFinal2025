 
from apps.assign.repositories.AsignationInstructorHistoryRepository import AsignationInstructorHistoryRepository

from apps.assign.entity.models import AsignationInstructor
from apps.general.entity.models import Instructor

class AsignationInstructorHistoryService:
    def __init__(self):
        self.repository = AsignationInstructorHistoryRepository()

    def list_by_asignation(self, asignation_instructor_id):
        return self.repository.list_by_asignation(asignation_instructor_id)

    def reasignar_instructor(self, asignation_instructor_id, new_instructor_id, message):
        from apps.security.entity.models import User
        from apps.security.emails.DesvinculacionInstructor import send_unassignment_to_instructor_email

        asignation_instructor = AsignationInstructor.objects.get(id=asignation_instructor_id)
        old_instructor = asignation_instructor.instructor
        old_instructor_id = old_instructor.id
        new_instructor = Instructor.objects.get(id=new_instructor_id)
        # Guardar historial antes de actualizar
        self.repository.create_history(
            asignation_instructor=asignation_instructor,
            old_instructor_id=old_instructor_id,
            message=message
        )
        # Enviar correo al instructor anterior
        old_person = old_instructor.person
        old_user = User.objects.filter(person=old_person).first()
        email = old_user.email if old_user else None
        nombre_instructor = f"{old_person.first_name} {old_person.first_last_name}"
        nombre_aprendiz = f"{asignation_instructor.request_asignation.aprendiz.person.first_name} {asignation_instructor.request_asignation.aprendiz.person.first_last_name}"
        if email:
            send_unassignment_to_instructor_email(email, nombre_instructor, nombre_aprendiz)
        # Actualizar asignación con el nuevo instructor
        asignation_instructor.instructor = new_instructor
        asignation_instructor.save()
        return asignation_instructor
