from apps.security.entity.models import Form
from core.base.serializers.implements.BaseSerializer import BaseSerializer


class FormSerializer(BaseSerializer):
    class Meta:
        model = Form
        fields = ['id', 'name', 'path', 'description', 'active']
