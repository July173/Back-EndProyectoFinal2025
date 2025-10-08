from apps.general.entity.models import Instructor
from apps.security.entity.models import Person
from apps.general.entity.models.TypeContract import TypeContract
from rest_framework import serializers


class InstructorSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    contractType = serializers.PrimaryKeyRelatedField(queryset=TypeContract.objects.all())

    class Meta:
        model = Instructor
        fields = [
            'id',
            'person',
            'contractType',
            'contractStartDate',
            'contractEndDate',
            'knowledgeArea',
            'active',
            'assigned_learners',
            'max_assigned_learners',
            'is_followup_instructor'
        ]
