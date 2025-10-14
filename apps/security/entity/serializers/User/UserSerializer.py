from apps.security.entity.models import User
from rest_framework import serializers
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.RoleSerializer import RoleSerializer
from apps.general.entity.serializers.CreateAprendiz.ApprenticeSerializer import ApprenticeSerializer
from apps.general.entity.serializers.CreateInstructor.InstructorSerializer import InstructorSerializer
from apps.general.entity.models import Apprentice, Instructor


class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    # Dynamic fields for apprentice and instructor
    aprendiz = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()

    def get_aprendiz(self, obj):
        aprendiz = Apprentice.objects.filter(person=obj.person).first()
        if aprendiz:
            return ApprenticeSerializer(aprendiz).data
        return None

    def get_instructor(self, obj):
        instructor = Instructor.objects.filter(person=obj.person).first()
        if instructor:
            return InstructorSerializer(instructor).data
        return None

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'person', 'role', 'is_active', 'registered', 'aprendiz', 'instructor']
        ref_name = "UserModelSerializer"
        extra_kwargs = {
            'password': {'write_only': True}
        }