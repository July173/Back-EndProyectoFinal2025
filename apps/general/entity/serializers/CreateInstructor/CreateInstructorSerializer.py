from rest_framework import serializers


class CreateInstructorSerializer(serializers.Serializer):
    # Campos de Person
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    type_identification = serializers.CharField()
    number_identification = serializers.CharField()
    # Campos de User
    email = serializers.EmailField()
    # Campos de Instructor
    contractType = serializers.CharField()
    contractStartDate = serializers.DateField()
    contractEndDate = serializers.DateField()
    knowledgeArea = serializers.IntegerField()
    # IDs de relación
    center_id = serializers.IntegerField()
    sede_id = serializers.IntegerField()
    regional_id = serializers.IntegerField()

    class Meta:
        ref_name = "CreateInstructorInputSerializer"
