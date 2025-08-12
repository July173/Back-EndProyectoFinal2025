from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.PersonRepository import PersonRepository


class PersonService(BaseService):
    def __init__(self):
        self.repository = PersonRepository()
