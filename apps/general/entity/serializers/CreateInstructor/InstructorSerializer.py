from apps.general.entity.models import Instructor
from apps.security.entity.models import Person
from apps.general.entity.models.TypeContract import TypeContract
from rest_framework import serializers


class InstructorSerializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(required=True)
    contract_type = serializers.IntegerField(required=True)

    class Meta:
        model = Instructor
        fields = [
            'id',
            'person_id',
            'contract_type',
            'contract_start_date',
            'contract_end_date',
            'knowledge_area',
            'active',
            'assigned_learners',
            'max_assigned_learners',
            'is_followup_instructor'
        ]
        extra_kwargs = {
            'assigned_learners': {'write_only': True},
            'max_assigned_learners': {'write_only': True},
        }
