from rest_framework import serializers
from apps.security.entity.models import Person


class PersonSerializer(serializers.ModelSerializer):

    # Permitir que la imagen sea opcional cuando se registra una persona
    image = serializers.ImageField(use_url=True, allow_null=True, required=False)
    
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
