from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.ModuleRepository import ModuleRepository


class ModuleService(BaseService):
    def __init__(self):
        self.repository = ModuleRepository()
    
    # method to get filtered modules
    def get_filtered_modules(self, active=None, search=None):
        return self.repository.get_filtered_modules(active, search)
