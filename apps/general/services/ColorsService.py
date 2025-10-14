from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.ColorsRepository import ColorsRepository

class ColorsService(BaseService):
    """
    Service for Colors entity operations.
    """
    def __init__(self):
        super().__init__(ColorsRepository())
