from apps.general.entity.models import Sede, Center
from rest_framework import serializers


class SedeSerializer(serializers.ModelSerializer):
    center = serializers.PrimaryKeyRelatedField(queryset=Center.objects.all())

    class Meta:
        model = Sede
        fields = [
            'id',
            'name',
            'codeSede',
            'address',
            'phoneSede',
            'emailContact',
            'center',
            'active',
        ]
