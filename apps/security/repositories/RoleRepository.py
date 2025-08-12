from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import Role


class RoleRepository(BaseRepository):
    def __init__(self):
        super().__init__(Role)
