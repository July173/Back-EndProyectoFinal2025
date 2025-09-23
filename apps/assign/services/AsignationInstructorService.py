# AsignationInstructorService.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.AsignationInstructorRepository import AsignationInstructorRepository
from apps.general.entity.models import Instructor
from apps.assign.entity.models import RequestAsignation


class AsignationInstructorService(BaseService):
    def create_custom(self, instructor_id, request_asignation_id):
        instructor = Instructor.objects.get(id=instructor_id)
        request_asignation = RequestAsignation.objects.get(id=request_asignation_id)
        asignation = self.repository.create_custom(instructor, request_asignation)
        return asignation
    def __init__(self):
        self.repository = AsignationInstructorRepository()
