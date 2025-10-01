from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.ColorsRepository import ColorsRepository

class ColorsService(BaseService):
    """
    Servicio para operaciones de negocio sobre Colors.
    """
    def __init__(self):
        self.repository = ColorsRepository()
