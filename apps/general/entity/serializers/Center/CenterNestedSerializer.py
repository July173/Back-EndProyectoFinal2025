from rest_framework import serializers
from apps.general.entity.models import Center, Sede

class SedeNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['id', 'name', 'codeSede', 'address', 'phoneSede', 'emailContact', 'active']

class CenterNestedSerializer(serializers.ModelSerializer):
    sedes = SedeNestedSerializer(many=True, read_only=True)
    
    class Meta:
        model = Center
        fields = ['id', 'name', 'codeCenter', 'address', 'active', 'sedes']