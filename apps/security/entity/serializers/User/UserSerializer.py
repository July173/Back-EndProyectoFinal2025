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
        # Buscar si la persona está vinculada como Apprentice
        from apps.general.entity.models import Apprentice, Ficha, Program
        aprendiz = Apprentice.objects.filter(person=obj.person).select_related('ficha__program').first()
        if aprendiz:
            data = ApprenticeSerializer(aprendiz).data
            ficha = aprendiz.ficha
            if ficha and ficha.program:
                data['programa'] = {
                    'id': ficha.program.id,
                    'name': ficha.program.name
                }
            else:
                data['programa'] = None
            return data
        return None

    def get_instructor(self, obj):
        # Buscar si la persona está vinculada como Instructor
        from apps.general.entity.models import Instructor, PersonSede, Sede, Center, Regional
        instructor = Instructor.objects.filter(person=obj.person).first()
        if instructor:
            data = InstructorSerializer(instructor).data
            # Buscar la sede vinculada
            person_sede = PersonSede.objects.filter(PersonId=instructor.person).select_related('SedeId__center__regional').first()
            if person_sede and person_sede.SedeId:
                sede = person_sede.SedeId
                centro = sede.center if hasattr(sede, 'center') else None
                regional = centro.regional if centro and hasattr(centro, 'regional') else None
                data['sede'] = {'id': sede.id, 'name': sede.name} if sede else None
                data['centro'] = {'id': centro.id, 'name': centro.name} if centro else None
                data['regional'] = {'id': regional.id, 'name': regional.name} if regional else None
            else:
                data['sede'] = None
                data['centro'] = None
                data['regional'] = None
            return data
        return None

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'person', 'role', 'is_active', 'registered', 'aprendiz', 'instructor']
        ref_name = "UserModelSerializer"
        extra_kwargs = {
            'password': {'write_only': True}
        }