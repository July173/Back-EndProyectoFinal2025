from apps.general.entity.models import PersonSede, Sede
from apps.security.entity.models import Person
from rest_framework import serializers


class PersonSedeSerializer(serializers.ModelSerializer):
    sede = serializers.IntegerField(required=True)
    person = serializers.IntegerField(required=True)

    class Meta:
        model = PersonSede
        fields = [
            'id',
            'sede',
            'person',
            'active',
        ]
