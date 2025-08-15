from apps.general.entity.models import Regional
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class RegionalSerializer(BaseSerializer):
    class Meta:
        model = Regional
        fields = ['id', 'name', 'codeRegional', 'description', 'active', 'address']
