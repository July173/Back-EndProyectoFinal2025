from rest_framework import serializers
from apps.general.entity.models import Instructor, PersonSede
from apps.security.entity.models import User


class GetInstructorSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    second_name = serializers.SerializerMethodField()
    first_last_name = serializers.SerializerMethodField()
    second_last_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    type_identification = serializers.SerializerMethodField()
    number_identification = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    role_id = serializers.SerializerMethodField()
    contractType = serializers.SerializerMethodField()  # Cambiado para devolver el ID
    contractStartDate = serializers.DateField()
    contractEndDate = serializers.DateField()
    knowledgeArea = serializers.SerializerMethodField()
    sede_id = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = [
            'id',
            'first_name',
            'second_name',
            'first_last_name',
            'second_last_name',
            'phone_number',
            'type_identification',
            'number_identification',
            'email',
            'role_id',
            'contractType',
            'contractStartDate',
            'contractEndDate',
            'knowledgeArea',
            'sede_id',
            'active'
        ]
    def get_first_name(self, obj):
        return obj.person.first_name if obj.person else None

    def get_second_name(self, obj):
        return obj.person.second_name if obj.person else None

    def get_first_last_name(self, obj):
        return obj.person.first_last_name if obj.person else None

    def get_second_last_name(self, obj):
        return obj.person.second_last_name if obj.person else None

    def get_phone_number(self, obj):
        return obj.person.phone_number if obj.person else None

    def get_type_identification(self, obj):
        # Devolver el ID del tipo de documento en lugar del objeto completo
        return obj.person.type_identification_id if obj.person else None

    def get_number_identification(self, obj):
        return obj.person.number_identification if obj.person else None

    def get_email(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.email if user else None

    def get_role_id(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.role.id if user and user.role else None
    
    def get_contractType(self, obj):
        # Devolver el ID del tipo de contrato en lugar del objeto completo
        return obj.contractType_id if obj.contractType_id else None

    def get_knowledgeArea(self, obj):
        return obj.knowledgeArea.id if obj.knowledgeArea else None

    def get_sede_id(self, obj):
        person_sede = PersonSede.objects.filter(PersonId=obj.person).first()
        if person_sede and person_sede.SedeId:
            return person_sede.SedeId.id
        return None

    def get_active(self, obj):
        user = User.objects.filter(person=obj.person).first()
        return user.is_active if user else False
