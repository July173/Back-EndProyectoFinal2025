from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.CenterRepository import CenterRepository


class CenterService(BaseService):
    def __init__(self):
        self.repository = CenterRepository()
    
    def get_center_with_sedes_by_id(self, pk):
        """Obtiene un centro por ID con sus sedes anidadas"""
        from apps.general.entity.models import Center
        try:
            return Center.objects.prefetch_related('sedes').get(pk=pk)
        except Center.DoesNotExist:
            return None
    
    def get_all_centers_with_sedes(self):
        """Obtiene todos los centros con sus sedes anidadas"""
        from apps.general.entity.models import Center
        return Center.objects.prefetch_related('sedes').all()
