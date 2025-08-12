from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Center


class CenterRepository(BaseRepository):
    def __init__(self):
        super().__init__(Center)
