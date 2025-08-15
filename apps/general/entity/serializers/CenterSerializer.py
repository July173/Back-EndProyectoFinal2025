from apps.general.entity.models import Center
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class CenterSerializer(BaseSerializer):
    class Meta:
        model = Center
        fields = ['id', 'name', 'codeCenter', 'address', 'active']
