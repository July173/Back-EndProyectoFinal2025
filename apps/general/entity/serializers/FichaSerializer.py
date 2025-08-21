from apps.general.entity.models import Ficha, Program
from rest_framework import serializers


class FichaSerializer(serializers.ModelSerializer):
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())

    class Meta:
        model = Ficha
        fields = [
            'id',
            'numeroFicha',
            'program',
            'active'
        ]
