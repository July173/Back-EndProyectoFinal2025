from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.ModuleService import ModuleService
from apps.security.entity.serializers.ModuleSerializer import ModuleSerializer


class ModuleViewSet(BaseViewSet):
    service_class = ModuleService
    serializer_class = ModuleSerializer
