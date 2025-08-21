from rest_framework import serializers


class CreateInstructorFlatSerializer(serializers.Serializer):
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
    password = serializers.CharField()
    role_id = serializers.IntegerField()
    # Campos de Instructor
    contractType = serializers.CharField()
    contractStartDate = serializers.CharField()
    contractEndDate = serializers.CharField()
    knowledgeArea = serializers.CharField()

    class Meta:
        ref_name = "CreateInstructorFlatInputSerializer"
