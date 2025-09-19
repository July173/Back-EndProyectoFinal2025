from rest_framework import serializers
from apps.security.entity.models import Person
from apps.security.entity.enums.document_type_enum import DocumentType


class PersonSerializer(serializers.ModelSerializer):

    # Permitir que la imagen sea opcional cuando se registra una persona
    image = serializers.ImageField(use_url=True, allow_null=True, required=False)
    choices_type_identification = [(doc_type.name, doc_type.value) for doc_type in DocumentType]
    print("Choices para type_identification:", choices_type_identification)
    type_identification = serializers.ChoiceField(choices=choices_type_identification)

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
