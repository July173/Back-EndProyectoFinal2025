from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.RegionalRepository import RegionalRepository
from apps.general.entity.models import Regional


class RegionalService(BaseService):
    def __init__(self):
        self.repository = RegionalRepository()
    
    def get_regional_with_centers_by_id(self, pk):
        """
        Get a regional by ID with its nested centers.
        Returns the Regional object or None if not found.
        """
        try:
            return Regional.objects.prefetch_related('centers').get(pk=pk)
        except Regional.DoesNotExist:
            return None

    def get_all_regionals_with_centers(self):
        """
        Get all regionals with their nested centers.
        Returns a queryset of all Regional objects with centers prefetched.
        """
        return Regional.objects.prefetch_related('centers').all()
