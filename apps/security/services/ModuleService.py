from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.ModuleRepository import ModuleRepository


class ModuleService(BaseService):
    def __init__(self):
        self.repository = ModuleRepository()
