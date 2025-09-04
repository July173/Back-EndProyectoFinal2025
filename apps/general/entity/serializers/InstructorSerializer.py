from apps.general.entity.models import Instructor
from apps.security.entity.models import Person
from rest_framework import serializers


class InstructorSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())

    class Meta:
        model = Instructor
        fields = [
            'id',
            'person',
            'contractType',
            'contractStartDate',
            'contractEndDate',
            'knowledgeArea',
            'active'
        ]
