from apps.security.entity.models import Module
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class ModuleSerializer(BaseSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'description', 'active']
