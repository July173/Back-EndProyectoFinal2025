from apps.security.entity.models import Role
from core.base.serializers.implements.BaseSerializer import BaseSerializer


class RoleSerializer(BaseSerializer):
    class Meta:
        model = Role
        fields = ['id', 'type_role', 'description', 'active']
