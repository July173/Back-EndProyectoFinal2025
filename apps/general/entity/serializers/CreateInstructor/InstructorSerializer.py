from apps.general.entity.models import Instructor
from apps.security.entity.models import Person
from apps.general.entity.enums.contract_type_enum import ContractType
from rest_framework import serializers


class InstructorSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    contractType = serializers.ChoiceField(choices=[ct.name for ct in ContractType])

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
