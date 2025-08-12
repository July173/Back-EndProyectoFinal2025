from apps.security.entity.models import Form
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class FormSerializer(BaseSerializer):
    class Meta:
        model = Form
        fields = ['id', 'name', 'description', 'active']
