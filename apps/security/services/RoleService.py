# apps/security/services/role_service.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleRepository import RoleRepository


class RoleService(BaseService):
    def __init__(self):
        self.repository = RoleRepository()
