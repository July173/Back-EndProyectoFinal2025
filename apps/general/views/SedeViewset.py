from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.SedeService import SedeService
from apps.general.entity.serializers.SedeSerializer import SedeSerializer


class SedeViewSet(BaseViewSet):
    service_class = SedeService
    serializer_class = SedeSerializer
