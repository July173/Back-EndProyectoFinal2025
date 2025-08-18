from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Program


class ProgramRepository(BaseRepository):
    def __init__(self):
        super().__init__(Program)
