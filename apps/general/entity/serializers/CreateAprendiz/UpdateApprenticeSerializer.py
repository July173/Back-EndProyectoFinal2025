from rest_framework import serializers
from apps.security.entity.models.DocumentType import DocumentType

class UpdateApprenticeSerializer(serializers.Serializer):
    type_identification = serializers.PrimaryKeyRelatedField(queryset=DocumentType.objects.all())
    number_identification = serializers.IntegerField(required=True)
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    program_id = serializers.IntegerField()
    ficha_id = serializers.IntegerField()
    role_id = serializers.IntegerField(required=False)