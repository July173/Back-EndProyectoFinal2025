from apps.general.entity.models import Apprentice, Ficha
from apps.security.entity.models import Person
from rest_framework import serializers


class ApprenticeSerializer(serializers.ModelSerializer):
    person_id = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    ficha_id = serializers.PrimaryKeyRelatedField(queryset=Ficha.objects.all())

    class Meta:
        model = Apprentice
        fields = [
            'id',
            'person_id',
            'ficha_id',
            'active'
        ]
