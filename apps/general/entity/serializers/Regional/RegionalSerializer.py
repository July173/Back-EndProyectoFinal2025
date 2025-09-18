from apps.general.entity.models import Regional
from rest_framework import serializers


class RegionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regional
        fields = [
            'id',
            'name',
            'codeRegional',
            'description',
            'active',
            'address'
        ]
