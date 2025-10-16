from apps.general.entity.models import Apprentice, Ficha
from apps.security.entity.models import Person
from rest_framework import serializers


class ApprenticeSerializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(required=True)
    ficha_id = serializers.IntegerField(required=True)

    class Meta:
        model = Apprentice
        fields = [
            'id',
            'person',
            'ficha',
            'active'
        ]
