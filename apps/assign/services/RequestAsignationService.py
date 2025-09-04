# RequestAsignationService.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.RequestAsignationRepository import RequestAsignationRepository


class RequestAsignationService(BaseService):
    def __init__(self):
        self.repository = RequestAsignationRepository()
