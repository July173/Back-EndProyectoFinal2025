from apps.general.entity.models import Center, Regional
from rest_framework import serializers


class CenterSerializer(serializers.ModelSerializer):
    regional = serializers.PrimaryKeyRelatedField(queryset=Regional.objects.all())

    class Meta:
        model = Center
        fields = [
            'id',
            'name',
            'code_center',
            'address',
            'active',
            'regional'
        ]
