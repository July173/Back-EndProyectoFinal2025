from apps.assign.repositories.VisitFollowingRepository import VisitFollowingRepository

class VisitFollowingService:
    def __init__(self):
        self.repository = VisitFollowingRepository()

    def get(self):
        return self.repository.get()

    def get_by_id(self, pk):
        obj = self.repository.get_by_id(pk)
        if not obj:
            return {"status": "error", "type": "not_found", "detail": f"No existe una visita de seguimiento con id {pk}."}
        return obj

    def create(self, validated_data):
        required_fields = [
            'visit_number', 'observations', 'state_visit', 'scheduled_date',
            'name_visit', 'asignation_instructor'
        ]
        for field in required_fields:
            if not validated_data.get(field):
                return {
                    "status": "error",
                    "type": "missing_data",
                    "detail": f"El campo '{field}' es obligatorio."
                }
        obj = self.repository.create(**validated_data)
        return obj

    def update(self, pk, validated_data):
        # Validate existence
        obj = self.repository.get_by_id(pk)
        if not obj:
            return {"status": "error", "type": "not_found", "detail": f"No existe una visita de seguimiento con id {pk}."}
        # Validate required fields if updating
        required_fields = [
            'visit_number', 'observations', 'state_visit', 'scheduled_date',
            'name_visit', 'asignation_instructor'
        ]
        for field in required_fields:
            if field in validated_data and not validated_data.get(field):
                return {
                    "status": "error",
                    "type": "missing_data",
                    "detail": f"El campo '{field}' es obligatorio para actualizar."
                }
        obj = self.repository.update(pk, **validated_data)
        return obj
