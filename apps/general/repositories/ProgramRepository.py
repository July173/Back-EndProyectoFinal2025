from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Program, Ficha
from django.utils import timezone
from django.db import transaction


class ProgramRepository(BaseRepository):
    """
    Repository for managing program and related ficha logic.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """

    def __init__(self):
        super().__init__(Program)

    def get_fichas_by_program(self, program_id):
        """
        Return all fichas linked to a specific program, without filtering by state.
        """
        return Ficha.objects.filter(program_id=program_id)

    def set_active_state_program_with_fichas(self, program_id, active=True):
        """
        Activate or deactivate a program and all its linked fichas.
        If active=True, activate; if active=False, deactivate.
        """
        try:
            with transaction.atomic():
                program = self.model.objects.filter(pk=program_id).first()
                if not program:
                    return False

                program.active = active
                program.delete_at = None if active else timezone.now()
                program.save()

                # Update all linked fichas
                fichas = Ficha.objects.filter(program_id=program_id)
                for ficha in fichas:
                    ficha.active = active
                    ficha.delete_at = None if active else timezone.now()
                    ficha.save()

                return True
        except Exception as e:
            print(f"Error in set_active_state_program_with_fichas: {e}")
            return False
