from apps.general.entity.models import Sede
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class SedeSerializer(BaseSerializer):
    class Meta:
        model = Sede
        fields = ['id', 'name', 'codeSede', 'address', 'phoneSede', 'emailContact', 'active']
