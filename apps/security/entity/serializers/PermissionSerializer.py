from apps.security.entity.models import Permission
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class PermissionSerializer(BaseSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'type_permission', 'description']
