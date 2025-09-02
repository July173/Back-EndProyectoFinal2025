from rest_framework import serializers

class UpdateAprendizSerializer(serializers.Serializer):
    type_identification = serializers.CharField()
    number_identification = serializers.CharField()
    first_name = serializers.CharField()
    second_name = serializers.CharField(required=False, allow_blank=True)
    first_last_name = serializers.CharField()
    second_last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    program_id = serializers.IntegerField()
    ficha_id = serializers.IntegerField()
    role_id = serializers.IntegerField()