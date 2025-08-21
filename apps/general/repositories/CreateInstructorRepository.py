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
