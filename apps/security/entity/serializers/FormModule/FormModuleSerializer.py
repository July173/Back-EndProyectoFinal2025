from apps.security.entity.models import FormModule
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class FormModuleSerializer(BaseSerializer):
    class Meta:
        model = FormModule
        fields = ['id', 'form', 'module', ]
