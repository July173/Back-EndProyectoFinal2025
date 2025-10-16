from apps.general.entity.models import Apprentice, Ficha
from apps.security.entity.models import Person
from rest_framework import serializers


class ApprenticeSerializer(serializers.ModelSerializer):
    person = serializers.IntegerField(required=True)
    ficha = serializers.IntegerField(required=True)

    class Meta:
        model = Apprentice
        fields = [
            'id',
            'person',
            'ficha',
            'active'
        ]
