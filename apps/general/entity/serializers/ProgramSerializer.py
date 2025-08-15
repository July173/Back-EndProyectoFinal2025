from apps.general.entity.models import Program
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class ProgramSerializer(BaseSerializer):
    class Meta:
        model = Program
        fields = ['id', 'codeProgram', 'name', 'typeProgram', 'description', 'active']
