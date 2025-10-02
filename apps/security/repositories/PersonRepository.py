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
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            person = serializer.save()
            return person, serializer.data, None
        return None, None, serializer.errors

    def delete_person(self, person):
        person.delete()
