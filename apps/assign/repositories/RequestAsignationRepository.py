from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import RequestAsignation


class RequestAsignationRepository(BaseRepository):
    def __init__(self):
        super().__init__(RequestAsignation)
