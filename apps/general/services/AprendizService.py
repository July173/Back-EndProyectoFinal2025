from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.AprendizRepository import AprendizRepository


class AprendizService(BaseService):
    def __init__(self):
        self.repository = AprendizRepository()
