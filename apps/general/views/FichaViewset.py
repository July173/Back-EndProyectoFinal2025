from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.FichaService import FichaService
from apps.general.entity.serializers.FichaSerializer import FichaSerializer


class FichaViewSet(BaseViewSet):
    service_class = FichaService
    serializer_class = FichaSerializer
