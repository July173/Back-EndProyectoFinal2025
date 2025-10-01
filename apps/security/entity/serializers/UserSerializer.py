from apps.security.entity.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'person', 'role', 'is_active', 'registered']
        ref_name = "UserModelSerializer"
