from apps.general.entity.models import Ficha
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class FichaSerializer(BaseSerializer):
    class Meta:
        model = Ficha
        fields = ['id', 'numeroFicha', 'active']
