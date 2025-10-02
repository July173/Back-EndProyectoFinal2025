from rest_framework import serializers
from apps.security.entity.models import Person

from apps.security.entity.models.DocumentType import DocumentType

class PersonSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_null=True, required=False)
    # Usar IntegerField para recibir el id del tipo de documento
    type_identification = serializers.IntegerField()

    class Meta:
        model = Person
        fields = [
            'id',
            'first_name',
            'second_name',
            'first_last_name',
            'second_last_name',
            'phone_number',
            'type_identification',
            'number_identification',
            'active',
            'image'
        ]
        ref_name = "PersonModelSerializer"
    
    def validate_type_identification(self, value):
        """Validar que el tipo de documento exista y esté activo"""
        if not DocumentType.objects.filter(pk=value, active=True).exists():
            raise serializers.ValidationError("Tipo de identificación inválido")
        return value
