from apps.general.entity.models import Sede, Center
from rest_framework import serializers


class SedeSerializer(serializers.ModelSerializer):
    center = serializers.IntegerField(required=True)

    class Meta:
        model = Sede
        fields = [
            'id',
            'name',
            'code_sede',
            'address',
            'phone_sede',
            'email_contact',
            'center',
            'active',
        ]
