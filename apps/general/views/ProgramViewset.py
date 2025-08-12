from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.ProgramService import ProgramService
from apps.general.entity.serializers.ProgramSerializer import ProgramSerializer


class ProgramViewSet(BaseViewSet):
    service_class = ProgramService
    serializer_class = ProgramSerializer
