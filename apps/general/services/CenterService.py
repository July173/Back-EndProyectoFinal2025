from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.CenterRepository import CenterRepository


class CenterService(BaseService):
    def __init__(self):
        self.repository = CenterRepository()
