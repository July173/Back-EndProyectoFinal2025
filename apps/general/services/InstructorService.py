from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.InstructorRepository import InstructorRepository


class InstructorService(BaseService):
    def __init__(self):
        self.repository = InstructorRepository()
