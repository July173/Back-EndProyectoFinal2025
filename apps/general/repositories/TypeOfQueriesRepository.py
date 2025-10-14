from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.TypeOfQueries import TypeOfQueries

class TypeOfQueriesRepository(BaseRepository): 
    def __init__(self):
        super().__init__(TypeOfQueries)
