from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.FormModuleRepository import FormModuleRepository


class FormModuleService(BaseService):
    def __init__(self):
        self.repository = FormModuleRepository()
