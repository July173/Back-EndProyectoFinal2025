from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleFormPermissionRepository import RolFormPermissionRepository


class RolFormPermissionService(BaseService):
    def __init__(self):
        self.repository = RolFormPermissionRepository()
