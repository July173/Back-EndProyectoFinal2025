from apps.general.entity.models import Sede, Center
from rest_framework import serializers


class SedeSerializer(serializers.ModelSerializer):
    center_id = serializers.PrimaryKeyRelatedField(queryset=Center.objects.all())

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
