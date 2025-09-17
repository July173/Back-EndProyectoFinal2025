from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Program


class ProgramRepository(BaseRepository):
    def __init__(self):
        super().__init__(Program)

    def get_fichas_by_program(self, program_id):
        """
        Retorna todas las fichas vinculadas a un programa específico.
        """
        from apps.general.entity.models import Ficha
        return Ficha.objects.filter(program_id=program_id, active=True)
