from apps.general.entity.models import Aprendiz, Ficha
from apps.security.entity.models import Person
from rest_framework import serializers


class AprendizSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    ficha = serializers.PrimaryKeyRelatedField(queryset=Ficha.objects.all())

    class Meta:
        model = Aprendiz
        fields = [
            'id',
            'person',
            'ficha',
            'active'
        ]
