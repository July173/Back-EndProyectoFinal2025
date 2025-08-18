from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.RegionalRepository import RegionalRepository


class RegionalService(BaseService):
    def __init__(self):
        self.repository = RegionalRepository()
