# AsignationInstructorService.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.AsignationInstructorRepository import AsignationInstructorRepository


class AsignationInstructorService(BaseService):
    def __init__(self):
        self.repository = AsignationInstructorRepository()
