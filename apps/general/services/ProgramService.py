from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.ProgramRepository import ProgramRepository


class ProgramService(BaseService):
    def __init__(self):
        self.repository = ProgramRepository()

    def get_fichas_by_program(self, program_id):
        """
        Returns the records (fichas) linked to a specific program.
        """
        return self.repository.get_fichas_by_program(program_id)

    def logical_delete_program(self, program_id):
        """
        Performs logical deletion or reactivation of a program and its linked records (fichas).
        User-facing messages remain in Spanish.
        """
        program = self.get(program_id)
        if not program:
            raise ValueError(f"Programa con ID {program_id} no encontrado")
        if not program.active:
            self.repository.set_active_state_program_with_fichas(program_id, active=True)
            return "Programa reactivado correctamente."
        else:
            self.repository.set_active_state_program_with_fichas(program_id, active=False)
            return "Eliminación lógica realizada correctamente."
