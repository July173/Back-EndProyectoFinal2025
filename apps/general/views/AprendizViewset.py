from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.AprendizService import AprendizService
from apps.general.entity.serializers.AprendizSerializer import AprendizSerializer


class AprendizViewSet(BaseViewSet):
    service_class = AprendizService
    serializer_class = AprendizSerializer
