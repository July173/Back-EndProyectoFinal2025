from rest_framework import serializers
from apps.security.entity.enums.document_type_enum import DocumentType
from apps.general.entity.enums.contract_type_enum import ContractType


class CreateInstructorSerializer(serializers.Serializer):
    # Campos de Person
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.IntegerField(required=False)
    type_identification = serializers.ChoiceField(choices=[dt.name for dt in DocumentType])
    number_identification = serializers.IntegerField(required=True)
    # Campos de User
    email = serializers.EmailField()
    role_id = serializers.IntegerField()
    # Campos de Instructor
    contractType = serializers.ChoiceField(choices=[ct.name for ct in ContractType])
    contractStartDate = serializers.DateField()
    contractEndDate = serializers.DateField()
    knowledgeArea = serializers.IntegerField()
    # ID de relación
    sede_id = serializers.IntegerField()

    class Meta:
        ref_name = "CreateInstructorInputSerializer"
