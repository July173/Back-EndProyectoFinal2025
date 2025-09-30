# AsignationInstructorService.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.AsignationInstructorRepository import AsignationInstructorRepository
from apps.general.entity.models import Instructor
from apps.assign.entity.models import RequestAsignation
from apps.assign.entity.enums.request_state_enum import RequestState
from apps.security.entity.models import User
from apps.security.emails.AsignacionInstructor import send_instructor_assignment_email
from apps.security.emails.AsignacionInstructor import send_assignment_to_instructor_email



class AsignationInstructorService(BaseService):
    def __init__(self):
        self.repository = AsignationInstructorRepository()


    def create_custom(self, instructor_id, request_asignation_id):
        instructor = Instructor.objects.get(id=instructor_id)
        request_asignation = RequestAsignation.objects.get(id=request_asignation_id)
        # Validar que el estado no sea RECHAZADO
        if request_asignation.request_state == RequestState.RECHAZADO:
            raise ValueError("No se puede asignar un instructor a una solicitud rechazada.")
        asignation = self.repository.create_custom(instructor, request_asignation)
        request_asignation.request_state = RequestState.ASIGNADO
        request_asignation.save()
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

