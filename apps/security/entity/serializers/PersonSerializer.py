from apps.security.entity.models import Person
from core.base.serializers.implements.baseSerializer.BaseSerializer import BaseSerializer


class PersonSerializer(BaseSerializer):
    class Meta:
        model = Person
        fields = [
            'id',
            'first_name',
            'second_name',
            'first_last_name',
            'second_last_name',
            'phone_number',
            'type_identification',
            'number_identification',
            'active',
        ]
