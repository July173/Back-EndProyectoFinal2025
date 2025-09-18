from rest_framework import serializers
from apps.security.entity.enums.document_type_enum import DocumentType

class UpdateAprendizSerializer(serializers.Serializer):
    type_identification = serializers.ChoiceField(choices=[dt.value for dt in DocumentType])
    number_identification = serializers.IntegerField(required=True)
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    program_id = serializers.IntegerField()
    ficha_id = serializers.IntegerField()
    role_id = serializers.IntegerField()