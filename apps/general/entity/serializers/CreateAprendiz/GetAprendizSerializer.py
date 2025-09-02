from rest_framework import serializers
from apps.general.entity.models import Aprendiz, Ficha, Program
from apps.security.entity.models import User, Role

class GetAprendizSerializer(serializers.ModelSerializer):
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
            'estado'
        ]

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
        return obj.ficha.numeroFicha if obj.ficha else None

    def get_estado(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return "Registrado" if user and user.is_active else "Inactivo"