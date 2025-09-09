from apps.security.entity.models import RolFormPermission
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class RolFormPermissionSerializer(BaseSerializer):
    class Meta:
        model = RolFormPermission
        fields = ['id', 'role', 'form', 'permission']
