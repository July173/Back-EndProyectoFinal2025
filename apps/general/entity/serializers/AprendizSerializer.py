from apps.general.entity.models import Aprendiz
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class AprendizSerializer(BaseSerializer):
    class Meta:
        model = Aprendiz
        fields = ['id', 'active']
