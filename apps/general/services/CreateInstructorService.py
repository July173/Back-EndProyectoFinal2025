from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from apps.general.repositories.InstructorRepository import InstructorRepository
from apps.general.entity.serializers import CreateInstructorSerializer


class CreateInstructorService:
    def __init__(self, db: Session):
        self.repo = InstructorRepository(db)
        self.db = db

    def create_instructor(self, dto: CreateInstructorSerializer):
        try:
            with self.db.begin():
                person = self.repo.create_person(dto.person.dict())
                user_data = dto.user.dict()
                user_data['person_id'] = person.id
                user = self.repo.create_user(user_data)
                instructor_data = dto.instructor.dict()
                instructor_data['user_id'] = user.id
                instructor = self.repo.create_instructor(instructor_data)
                return {
                    "person_id": person.id,
                    "user_id": user.id,
                    "instructor_id": instructor.id
                }
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            raise Exception(f"Error al crear instructor: {str(e)}")
