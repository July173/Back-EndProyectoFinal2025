from rest_framework import serializers
from apps.general.entity.models import Regional, Center

class CenterForRegionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['id', 'name', 'codeCenter', 'address', 'active']

class RegionalNestedSerializer(serializers.ModelSerializer):
    centers = CenterForRegionalSerializer(many=True, read_only=True)
    class Meta:
        model = Regional
        fields = ['id', 'name', 'codeRegional', 'description', 'active', 'address', 'centers']
