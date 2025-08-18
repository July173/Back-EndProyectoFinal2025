from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Instructor


class InstructorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Instructor)
