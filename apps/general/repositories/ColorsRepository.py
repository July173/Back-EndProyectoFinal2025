from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.Colors import Colors

class ColorsRepository(BaseRepository):
    """
    Repository for CRUD operations on Colors.
    """
    def __init__(self):
        super().__init__(Colors)
