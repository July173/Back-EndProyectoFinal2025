from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import Module


class ModuleRepository(BaseRepository):
    def __init__(self):
        super().__init__(Module)
