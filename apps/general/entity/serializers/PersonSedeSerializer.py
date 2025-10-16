from apps.general.entity.models import PersonSede, Sede
from apps.security.entity.models import Person
from rest_framework import serializers


class PersonSedeSerializer(serializers.ModelSerializer):
    sede_id = serializers.PrimaryKeyRelatedField(queryset=Sede.objects.all())
    person_id = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())

    class Meta:
        model = PersonSede
        fields = [
            'id',
            'sede',
            'person',
            'active',
        ]
