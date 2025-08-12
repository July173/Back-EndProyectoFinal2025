from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.FormService import FormService
from apps.security.entity.serializers.FormSerializer import FormSerializer


class FormViewSet(BaseViewSet):
    service_class = FormService
    serializer_class = FormSerializer
