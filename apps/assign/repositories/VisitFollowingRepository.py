from apps.assign.entity.models import VisitFollowing

class VisitFollowingRepository:
    
    def get(self):
        return VisitFollowing.objects.all()
