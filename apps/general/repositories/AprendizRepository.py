from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Aprendiz


class AprendizRepository(BaseRepository):
    def __init__(self):
        super().__init__(Aprendiz)
