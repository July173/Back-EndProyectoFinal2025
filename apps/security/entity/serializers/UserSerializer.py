from apps.security.entity.models import User
from core.base.serializers.implements.BaseSerializer import BaseSerializer


class UserSerializer(BaseSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'person', 'role', 'is_active', 'registered']
        ref_name = "UserModelSerializer"
