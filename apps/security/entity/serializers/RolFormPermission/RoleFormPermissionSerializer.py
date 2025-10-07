from apps.security.entity.models import RolFormPermission
from rest_framework import serializers


class RolFormPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolFormPermission
        fields = ['id', 'role', 'form', 'permission']
