from apps.security.entity.models import User
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class UserSerializer(BaseSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'person', 'role']
