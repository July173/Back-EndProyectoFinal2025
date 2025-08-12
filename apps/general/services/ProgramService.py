from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.ProgramRepository import ProgramRepository


class ProgramService(BaseService):
    def __init__(self):
        self.repository = ProgramRepository()
