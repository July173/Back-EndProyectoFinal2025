from rest_framework import serializers
from apps.general.entity.models import Apprentice
from apps.security.entity.models import User

class GetApprenticeSerializer(serializers.ModelSerializer):
    # Usar type_identification_id para obtener el ID en lugar del objeto completo
    type_identification = serializers.IntegerField(source='person.type_identification_id')
    number_identification = serializers.CharField(source='person.number_identification')
    first_name = serializers.CharField(source='person.first_name')
    second_name = serializers.CharField(source='person.second_name')
    first_last_name = serializers.CharField(source='person.first_last_name')
    second_last_name = serializers.CharField(source='person.second_last_name')
    phone_number = serializers.CharField(source='person.phone_number')
    email = serializers.SerializerMethodField()
    program_id = serializers.IntegerField(source='ficha.program_id', required=False)
    ficha_id = serializers.IntegerField(source='ficha.id', required=False)
    role_id = serializers.SerializerMethodField()

    class Meta:
        model = Apprentice
        fields = [
            'id',
            'type_identification',
            'number_identification',
            'first_name',
            'second_name',
            'first_last_name',
            'second_last_name',
            'phone_number',
            'email',
            'program_id',
            'ficha_id',
            'role_id'
        ]

    def get_email(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.email if user else None

    def get_role_id(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.role.id if user and user.role else None