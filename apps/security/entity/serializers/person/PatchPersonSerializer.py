from rest_framework import serializers
from apps.security.entity.models import Person


class PatchPersonSerializer(serializers.ModelSerializer):
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
            'image',
        ]
        extra_kwargs = {
            'first_name': {'required': False},
            'second_name': {'required': False},
            'first_last_name': {'required': False},
            'second_last_name': {'required': False},
            'phone_number': {'required': False},
            'type_identification': {'required': False},
            'number_identification': {'required': False},
            'active': {'required': False},
            'image': {'required': False},
        }
