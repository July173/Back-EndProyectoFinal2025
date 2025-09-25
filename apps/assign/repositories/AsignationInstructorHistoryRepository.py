from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models.AsignationInstructorHistory import AsignationInstructorHistory

class AsignationInstructorHistoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(AsignationInstructorHistory)

    def create_history(self, asignation_instructor, old_instructor_id, message, changed_by):
        return self.model.objects.create(
            asignation_instructor=asignation_instructor,
            old_instructor_id=old_instructor_id,
            message=message,
            changed_by=changed_by
        )

    def list_by_asignation(self, asignation_instructor_id):
        return self.model.objects.filter(asignation_instructor_id=asignation_instructor_id)
