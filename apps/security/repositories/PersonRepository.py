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
        
        # Validar con el serializer
        serializer = PersonSerializer(data=person_data)
        if serializer.is_valid():
            # Transformar type_identification a type_identification_id para el modelo
            person_data_copy = person_data.copy()
            if 'type_identification' in person_data_copy:
                person_data_copy['type_identification_id'] = person_data_copy.pop('type_identification')
            
            # Crear la persona usando los datos transformados
            person = Person.objects.create(**person_data_copy)
            
            # Serializar la respuesta manualmente para evitar problemas con la ForeignKey
            response_data = {
                'id': person.id,
                'first_name': person.first_name,
                'second_name': person.second_name,
                'first_last_name': person.first_last_name,
                'second_last_name': person.second_last_name,
                'phone_number': person.phone_number,
                'type_identification': person.type_identification_id,
                'number_identification': person.number_identification,
                'active': person.active,
                'image': person.image.url if person.image else None
            }
            
            return person, response_data, None
        return None, None, serializer.errors

    def delete_person(self, person):
        person.delete()
