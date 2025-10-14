from apps.general.entity.models import Apprentice, Ficha
from apps.security.entity.models import Person
from rest_framework import serializers


class ApprenticeSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    ficha = serializers.PrimaryKeyRelatedField(queryset=Ficha.objects.all())

    class Meta:
        model = Apprentice
        fields = [
            'id',
            'person',
            'ficha',
            'active'
        ]
