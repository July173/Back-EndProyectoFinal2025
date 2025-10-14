from rest_framework import serializers
from apps.general.entity.models import Instructor, PersonSede
from apps.security.entity.models import User


class GetInstructorSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving instructor data.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """
    first_name = serializers.SerializerMethodField()
    second_name = serializers.SerializerMethodField()
    first_last_name = serializers.SerializerMethodField()
    second_last_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    type_identification = serializers.SerializerMethodField()
    number_identification = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    role_id = serializers.SerializerMethodField()
    contractType = serializers.SerializerMethodField()  # Changed to return the ID
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
            'is_followup_instructor',
            'active',
        ]
        extra_kwargs = {
            'assigned_learners': {'write_only': True},
            'max_assigned_learners': {'write_only': True},
        }

    def get_first_name(self, obj):
        """Get the instructor's first name from the related person object."""
        return obj.person.first_name if obj.person else None

    def get_second_name(self, obj):
        """Get the instructor's second name from the related person object."""
        return obj.person.second_name if obj.person else None

    def get_first_last_name(self, obj):
        """Get the instructor's first last name from the related person object."""
        return obj.person.first_last_name if obj.person else None

    def get_second_last_name(self, obj):
        """Get the instructor's second last name from the related person object."""
        return obj.person.second_last_name if obj.person else None

    def get_phone_number(self, obj):
        """Get the instructor's phone number from the related person object."""
        return obj.person.phone_number if obj.person else None

    def get_type_identification(self, obj):
        """Return the ID of the document type instead of the full object."""
        return obj.person.type_identification_id if obj.person else None

    def get_number_identification(self, obj):
        """Get the instructor's identification number from the related person object."""
        return obj.person.number_identification if obj.person else None

    def get_email(self, obj):
        """Get the instructor's email from the related User object."""
        user = User.objects.filter(person=obj.person).first()
        return user.email if user else None

    def get_role_id(self, obj):
        """Get the role ID from the related User object."""
        user = User.objects.filter(person=obj.person).first()
        return user.role.id if user and user.role else None

    def get_contractType(self, obj):
        """Return the ID of the contract type instead of the full object."""
        return obj.contractType_id if obj.contractType_id else None

    def get_knowledgeArea(self, obj):
        """Get the knowledge area ID from the related object."""
        return obj.knowledgeArea.id if obj.knowledgeArea else None

    def get_sede_id(self, obj):
        """Get the site ID from the related PersonSede object."""
        person_sede = PersonSede.objects.filter(person_id=obj.person).first()
        if person_sede and person_sede.sede_id:
            return person_sede.sede_id.id
        return None

    def get_active(self, obj):
        """Get the active status from the related User object."""
        user = User.objects.filter(person=obj.person).first()
        return user.is_active if user else False
