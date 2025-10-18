from apps.assign.repositories.VisitFollowingRepository import VisitFollowingRepository

class VisitFollowingService:
    def __init__(self):
        self.repository = VisitFollowingRepository()

    def get(self):
        return self.repository.get()
