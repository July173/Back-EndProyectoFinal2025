from rest_framework import serializers
from apps.security.entity.models.DocumentType import DocumentType
from apps.general.entity.models.TypeContract import TypeContract


class CreateInstructorSerializer(serializers.Serializer):
    # Campos de Person
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.IntegerField(required=False)
    type_identification = serializers.PrimaryKeyRelatedField(queryset=DocumentType.objects.all())
    number_identification = serializers.IntegerField(required=True)
    # Campos de User
    email = serializers.EmailField()
    role_id = serializers.IntegerField()
    # Campos de Instructor
    contractType = serializers.PrimaryKeyRelatedField(queryset=TypeContract.objects.all())
    contractStartDate = serializers.DateField()
    contractEndDate = serializers.DateField()
    knowledgeArea = serializers.IntegerField()
    # ID de relación
    sede_id = serializers.IntegerField()

    class Meta:
        ref_name = "CreateInstructorInputSerializer"
