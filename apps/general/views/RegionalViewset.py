from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.RegionalService import RegionalService
from apps.general.entity.serializers.RegionalSerializer import RegionalSerializer


class RegionalViewSet(BaseViewSet):
    service_class = RegionalService
    serializer_class = RegionalSerializer
