from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.ProgramRepository import ProgramRepository


class ProgramService(BaseService):
    def __init__(self):
        self.repository = ProgramRepository()

    def get_fichas_by_program(self, program_id):
        """
        Devuelve las fichas vinculadas a un programa específico.
        """
        return self.repository.get_fichas_by_program(program_id)
