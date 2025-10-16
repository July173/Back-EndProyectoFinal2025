from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.ModuleRepository import ModuleRepository


class ModuleService(BaseService):
    def __init__(self):
        self.repository = ModuleRepository()
    
    # method to get filtered modules
    def get_filtered_modules(self, active=None, search=None):
        try:
            modules = self.repository.get_filtered_modules(active, search)
            if not modules.exists():
                raise ValueError("No se encontraron módulos con los filtros proporcionados.")
            return modules
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")
