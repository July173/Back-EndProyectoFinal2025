from rest_framework import serializers
from apps.security.entity.enums.document_type_enum import DocumentType

class CreateAprendizSerializer(serializers.Serializer):
    type_identification = serializers.ChoiceField(choices=[dt.name for dt in DocumentType])
    number_identification = serializers.IntegerField(required=True)
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    ficha_id = serializers.IntegerField()