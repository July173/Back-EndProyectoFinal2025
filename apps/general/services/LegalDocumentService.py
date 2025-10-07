from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.LegalDocumentRepository import LegalDocumentRepository

class LegalDocumentService(BaseService):
    def __init__(self):
        self.repository = LegalDocumentRepository()
