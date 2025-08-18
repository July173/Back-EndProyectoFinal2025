from apps.general.entity.models import Instructor
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class InstructorSerializer(BaseSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'contractType', 'contractStartDate', 'contractEndDate', 'knowledgeArea', 'active']
