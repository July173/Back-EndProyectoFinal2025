from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.ProgramRepository import ProgramRepository


class ProgramService(BaseService):
    def __init__(self):
        self.repository = ProgramRepository()

    def get_fichas_by_program(self, program_id):
        """
        Returns the records (fichas) linked to a specific program.
        """
        if not program_id:
            raise ValueError("Debes proporcionar un ID de programa válido.")
        fichas = self.repository.get_fichas_by_program(program_id)
        if not fichas.exists():
            raise ValueError("No se encontraron fichas vinculadas a este programa.")
        return fichas

    def logical_delete_program(self, program_id):
        """
        Performs logical deletion or reactivation of a program and its linked records (fichas).
        User-facing messages remain in Spanish.
        """
        try:
            program = self.get(program_id)
            if not program:
                raise ValueError(f"Programa con ID {program_id} no encontrado.")
            if not program.active:
                ok = self.repository.set_active_state_program_with_fichas(program_id, active=True)
                if not ok:
                    raise ValueError("No se pudo reactivar el programa. Intenta nuevamente.")
                return "Programa reactivado correctamente."
            else:
                ok = self.repository.set_active_state_program_with_fichas(program_id, active=False)
                if not ok:
                    raise ValueError("No se pudo realizar la eliminación lógica. Intenta nuevamente.")
                return "Eliminación lógica realizada correctamente."
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")
