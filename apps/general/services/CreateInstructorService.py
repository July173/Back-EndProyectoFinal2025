from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from apps.general.repositories.CreateInstructorRepository import CreateInstructorRepository
from apps.general.entity.models import Sede, Center, Regional, PersonSede
from apps.general.entity.serializers import CreateInstructorSerializer


class CreateInstructorService:
    def __init__(self, db: Session):
        self.repo = CreateInstructorRepository(db)
        self.db = db

    def create_instructor(self, dto: CreateInstructorSerializer):
        try:
            with self.db.begin():
                # Validar y obtener entidades relacionadas
                regional = self.db.query(Regional).filter_by(id=dto.regional_id).first()
                if not regional:
                    raise ValueError("Regional no encontrada")

                center = self.db.query(Center).filter_by(id=dto.center_id, regional_id=regional.id).first()
                if not center:
                    raise ValueError("Center no encontrada o no pertenece a la regional")

                sede = self.db.query(Sede).filter_by(id=dto.sede_id, center_id=center.id).first()
                if not sede:
                    raise ValueError("Sede no encontrada o no pertenece al centro")

                # Crear Person
                person_data = {
                    "first_name": dto.first_name,
                    "second_name": dto.second_name,
                    "first_last_name": dto.first_last_name,
                    "second_last_name": dto.second_last_name,
                    "phone_number": dto.phone_number,
                    "type_identification": dto.type_identification,
                    "number_identification": dto.number_identification
                }
                person = self.repo.create_person(person_data)

                # Relacionar Person con Sede (tabla pivote)
                sede_person = PersonSede(person_id=person.id, sede_id=sede.id)
                self.db.add(sede_person)

                # Crear User
                user_data = {
                    "email": dto.email,
                    "password": dto.password,
                    "role_id": dto.role_id,
                    "person_id": person.id
                }
                user = self.repo.create_user(user_data)

                # Crear Instructor
                instructor_data = {
                    "contractType": dto.contractType,
                    "contractStartDate": dto.contractStartDate,
                    "contractEndDate": dto.contractEndDate,
                    "knowledgeArea": dto.knowledgeArea,
                    "user_id": user.id
                }
                instructor = self.repo.create_instructor(instructor_data)

                return {
                    "person_id": person.id,
                    "user_id": user.id,
                    "instructor_id": instructor.id,
                    "sede_id": sede.id,
                    "center_id": center.id,
                    "regional_id": regional.id
                }
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            raise Exception(f"Error al crear instructor: {str(e)}")
