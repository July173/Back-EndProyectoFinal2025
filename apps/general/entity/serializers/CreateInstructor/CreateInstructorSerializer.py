from rest_framework import serializers
from apps.security.entity.models.DocumentType import DocumentType
from apps.general.entity.models.TypeContract import TypeContract


class CreateInstructorSerializer(serializers.Serializer):
    """
    Serializer for creating an instructor.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """
    # Person fields
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.IntegerField(required=False)
    type_identification = serializers.PrimaryKeyRelatedField(queryset=DocumentType.objects.all())
    number_identification = serializers.IntegerField(required=True)
    # User fields
    email = serializers.EmailField()
    role_id = serializers.IntegerField()
    # Instructor fields
    contract_type = serializers.PrimaryKeyRelatedField(queryset=TypeContract.objects.all())
    contract_start_date = serializers.DateField()
    contract_end_date = serializers.DateField()
    knowledge_area = serializers.IntegerField()
    # Relationship ID
    sede_id = serializers.IntegerField()
    is_followup_instructor = serializers.BooleanField(required=False, default=False)

    class Meta:
        ref_name = "CreateInstructorInputSerializer"
