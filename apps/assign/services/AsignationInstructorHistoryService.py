 
from apps.assign.repositories.AsignationInstructorHistoryRepository import AsignationInstructorHistoryRepository

from apps.assign.entity.models import AsignationInstructor
from apps.general.entity.models import Instructor

class AsignationInstructorHistoryService:
    def __init__(self):
        self.repository = AsignationInstructorHistoryRepository()

    def list_by_asignation(self, asignation_instructor_id):
        return self.repository.list_by_asignation(asignation_instructor_id)

    def reasignar_instructor(self, asignation_instructor_id, new_instructor_id, message):
        asignation_instructor = AsignationInstructor.objects.get(id=asignation_instructor_id)
        old_instructor_id = asignation_instructor.instructor.id
        new_instructor = Instructor.objects.get(id=new_instructor_id)
        # Guardar historial antes de actualizar
        self.repository.create_history(
            asignation_instructor=asignation_instructor,
            old_instructor_id=old_instructor_id,
            message=message
        )
        # Actualizar asignación con el nuevo instructor
        asignation_instructor.instructor = new_instructor
        asignation_instructor.save()
        return asignation_instructor
