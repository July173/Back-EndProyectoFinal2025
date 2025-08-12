from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
