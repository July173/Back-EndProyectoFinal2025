from apps.assign.repositories.AsignationInstructorHistoryRepository import AsignationInstructorHistoryRepository
from apps.assign.entity.models import AsignationInstructor
from apps.general.entity.models import Instructor
from apps.security.entity.models import User
from apps.assign.emails.DesvinculacionInstructor import send_unassignment_to_instructor_email
from apps.assign.emails.ReasignacionInstructor import send_assignment_to_new_instructor_email
from apps.assign.emails.DesvinculacionAprendiz import send_unassignment_to_aprendiz_email


class AsignationInstructorHistoryService:
    def __init__(self):
        self.repository = AsignationInstructorHistoryRepository()

    def list_by_asignation(self, asignation_instructor_id):
        return self.repository.list_by_asignation(asignation_instructor_id)

    def reasignar_instructor(self, asignation_instructor_id, new_instructor_id, message):
        
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
        old_email = old_user.email if old_user else None
        nombre_instructor = f"{old_person.first_name} {old_person.first_last_name}"
        aprendiz_person = asignation_instructor.request_asignation.aprendiz.person
        nombre_aprendiz = f"{aprendiz_person.first_name} {aprendiz_person.first_last_name}"
        if old_email:
            send_unassignment_to_instructor_email(old_email, nombre_instructor, nombre_aprendiz)
        # Enviar correo al instructor nuevo
        new_person = new_instructor.person
        new_user = User.objects.filter(person=new_person).first()
        new_email = new_user.email if new_user else None
        new_instructor_name = f"{new_person.first_name} {new_person.first_last_name}"
        if new_email:
            send_assignment_to_new_instructor_email(new_email, new_instructor_name, nombre_aprendiz)
        # Enviar correo al aprendiz
        aprendiz_user = User.objects.filter(person=aprendiz_person).first()
        aprendiz_email = aprendiz_user.email if aprendiz_user else None
        if aprendiz_email:
            send_unassignment_to_aprendiz_email(aprendiz_email, nombre_aprendiz)
        # Actualizar asignación con el nuevo instructor
        asignation_instructor.instructor = new_instructor
        asignation_instructor.save()
        return asignation_instructor
