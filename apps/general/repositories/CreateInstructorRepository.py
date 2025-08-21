from apps.security.entity.models import Person, User
from apps.general.entity.models import Instructor
from sqlalchemy.orm import Session


class CreateInstructorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_person(self, person_data: dict) -> Person:
        person = Person(**person_data)
        self.db.add(person)
        self.db.flush()
        return person

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.flush()
        return user

    def create_instructor(self, instructor_data: dict) -> Instructor:
        instructor = Instructor(**instructor_data)
        self.db.add(instructor)
        self.db.flush()
        return instructor

    def create_full_instructor(self, data: dict) -> dict:
        # Separar los datos
        person_fields = [
            'first_name', 'second_name', 'first_last_name', 'second_last_name',
            'phone_number', 'type_identification', 'number_identification'
        ]
        user_fields = ['email', 'password', 'role_id']
        instructor_fields = [
            'contractType', 'contractStartDate', 'contractEndDate', 'knowledgeArea',
            'center_id', 'sede_id', 'regional_id'
        ]

        person_data = {k: data[k] for k in person_fields}
        user_data = {k: data[k] for k in user_fields}
        instructor_data = {k: data[k] for k in instructor_fields}

        # Crear registros en orden y relacionarlos
        person = self.create_person(person_data)
        user_data['person_id'] = person.id
        user = self.create_user(user_data)
        instructor_data['user_id'] = user.id
        instructor = self.create_instructor(instructor_data)

        return {
            "person_id": person.id,
            "user_id": user.id,
            "instructor_id": instructor.id
        }
