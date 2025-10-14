from apps.security.entity.serializers.User.UserSimpleSerializer import UserSimpleSerializer
from apps.security.entity.models import User
from rest_framework import serializers
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.RoleSerializer import RoleSerializer
# Importar los serializers de Aprendiz e Instructor
from apps.general.entity.serializers.CreateAprendiz.ApprenticeSerializer import AprendizSerializer
from apps.general.entity.serializers.CreateInstructor.InstructorSerializer import InstructorSerializer

class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    # Campos dinámicos para aprendiz e instructor
    aprendiz = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()

    def get_aprendiz(self, obj):
        # Buscar si la persona está vinculada como Aprendiz
        from apps.general.entity.models import Aprendiz
        aprendiz = Aprendiz.objects.filter(person=obj.person).first()
        if aprendiz:
            return AprendizSerializer(aprendiz).data
        return None

    def get_instructor(self, obj):
        # Buscar si la persona está vinculada como Instructor
        from apps.general.entity.models import Instructor
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