from rest_framework import serializers
from apps.general.entity.models import Instructor
from apps.security.entity.models import User  # Ajusta el import si tu modelo User está en otro lugar


class GetInstructorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    knowledgeArea = serializers.CharField()
    role = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = [
            'id',
            'full_name',
            'email',
            'knowledgeArea',
            'role',
            'active'
        ]

    def get_full_name(self, obj):
        names = [
            obj.person.first_name,
            obj.person.second_name,
            obj.person.first_last_name,
            obj.person.second_last_name
        ]
        return " ".join([n for n in names if n])

    def get_email(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.email if user else None

    def get_role(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.role.type_role if user and user.role else None

    def get_active(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.is_active if user else False
