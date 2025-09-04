from rest_framework import serializers
from apps.security.entity.models import Person


class PersonSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

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
