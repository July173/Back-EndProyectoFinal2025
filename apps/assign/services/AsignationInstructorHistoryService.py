from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.AsignationInstructorHistoryRepository import AsignationInstructorHistoryRepository

class AsignationInstructorHistoryService(BaseService):
    def __init__(self):
        self.repository = AsignationInstructorHistoryRepository()

    def create_history(self, asignation_instructor, old_instructor_id, message, changed_by):
        return self.repository.create_history(asignation_instructor, old_instructor_id, message, changed_by)

    def list_by_asignation(self, asignation_instructor_id):
        return self.repository.list_by_asignation(asignation_instructor_id)
