from rest_framework import serializers
from apps.general.entity.models import Aprendiz
from apps.security.entity.models import User

class GetAprendizSerializer(serializers.ModelSerializer):
    type_identification = serializers.SerializerMethodField()
    number_identification = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    ficha = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Aprendiz
        fields = [
            'id',
            'full_name',
            'email',
            'program',
            'role',
            'ficha',
            'estado',
            'type_identification',
            'number_identification',
            'phone_number'
        ]
    def get_type_identification(self, obj):
        return obj.person.type_identification if obj.person else None

    def get_number_identification(self, obj):
        return obj.person.number_identification if obj.person else None

    def get_phone_number(self, obj):
        return obj.person.phone_number if obj.person else None

    def get_full_name(self, obj):
        person = obj.person
        names = [person.first_name, person.second_name, person.first_last_name, person.second_last_name]
        return " ".join([n for n in names if n])

    def get_email(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.email if user else None

    def get_program(self, obj):
        return obj.ficha.program.name if obj.ficha and obj.ficha.program else None

    def get_role(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.role.type_role if user and user.role else "Aprendiz"

    def get_ficha(self, obj):
        return obj.ficha.file_number if obj.ficha else None

    def get_estado(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return "Registrado" if user and user.is_active else "Inactivo"