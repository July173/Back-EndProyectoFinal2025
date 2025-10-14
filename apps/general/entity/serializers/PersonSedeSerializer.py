from apps.general.entity.models import PersonSede, Sede
from apps.security.entity.models import Person
from rest_framework import serializers


class PersonSedeSerializer(serializers.ModelSerializer):
    SedeId = serializers.PrimaryKeyRelatedField(queryset=Sede.objects.all())
    PersonId = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())

    class Meta:
        model = PersonSede
        fields = [
            'id',
            'sede_id',
            'person_id',
            'active',
        ]
