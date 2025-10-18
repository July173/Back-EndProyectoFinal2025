from apps.assign.entity.models import VisitFollowing

class VisitFollowingRepository:
    
    def get(self):
        return VisitFollowing.objects.all()

    def get_by_id(self, pk):
        try:
            return VisitFollowing.objects.get(id=pk)
        except VisitFollowing.DoesNotExist:
            return None

    def create(self, **kwargs):
        return VisitFollowing.objects.create(**kwargs)

    def update(self, pk, **kwargs):
        obj = self.get_by_id(pk)
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj
