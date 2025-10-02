from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import Person
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer


class PersonRepository(BaseRepository):
    def __init__(self):
        super().__init__(Person)

    def update_person(self, person, data):
        for attr, value in data.items():
            setattr(person, attr, value)
        person.save()
        return person

    def create_person(self, data):
        # Extraer solo los campos que pertenecen al modelo Person
        person_fields = {
            'first_name', 'second_name', 'first_last_name', 'second_last_name',
            'phone_number', 'type_identification', 'number_identification', 
            'active', 'image'
        }
        person_data = {k: v for k, v in data.items() if k in person_fields}
        
        # El serializer maneja automáticamente la conversión del ID a objeto DocumentType
        serializer = PersonSerializer(data=person_data)
        if serializer.is_valid():
            person = serializer.save()
            return person, serializer.data, None
        return None, None, serializer.errors

    def delete_person(self, person):
        person.delete()
