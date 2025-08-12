from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.FormModuleService import FormModuleService
from apps.security.entity.serializers.FormModuleSerializer import FormModuleSerializer


class FormModuleViewSet(BaseViewSet):
    service_class = FormModuleService
    serializer_class = FormModuleSerializer
