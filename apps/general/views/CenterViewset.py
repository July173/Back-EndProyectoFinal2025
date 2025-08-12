from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.CenterService import CenterService
from apps.general.entity.serializers.CenterSerializer import CenterSerializer


class CenterViewSet(BaseViewSet):
    service_class = CenterService
    serializer_class = CenterSerializer
