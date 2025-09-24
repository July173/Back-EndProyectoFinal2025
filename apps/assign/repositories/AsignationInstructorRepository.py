from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import AsignationInstructor


class AsignationInstructorRepository(BaseRepository):
    def create_custom(self, instructor, request_asignation):
        return self.model.objects.create(
            instructor=instructor,
            request_asignation=request_asignation
        )
    def __init__(self):
        super().__init__(AsignationInstructor)
