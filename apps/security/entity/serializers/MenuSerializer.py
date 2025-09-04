from rest_framework import serializers
from apps.security.entity.serializers.MenuFormSerializer import MenuFormSerializer

class MenuSerializer(serializers.Serializer):
    rol = serializers.CharField()
    moduleForm = MenuFormSerializer(many=True)