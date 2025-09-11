from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.general.entity.models import Instructor, PersonSede
from apps.security.entity.models import User

class Command(BaseCommand):
    help = 'Desactiva instructores y sus datos si el contrato ha finalizado.'

    def handle(self, *args, **options):
        hoy = timezone.now().date()
        instructores_vencidos = Instructor.objects.filter(contractEndDate__lte=hoy, active=True)
        total = instructores_vencidos.count()
        for instructor in instructores_vencidos:
            instructor.active = False
            instructor.delete_at = timezone.now()
            instructor.save()
            # Desactivar persona
            person = instructor.person
            person.active = False
            person.delete_at = timezone.now()
            person.save()
            # Desactivar usuario
            user = User.objects.filter(person=person).first()
            if user:
                user.is_active = False
                user.deleted_at = timezone.now()
                user.save()
            # Desactivar PersonSede
            person_sedes = PersonSede.objects.filter(PersonId=person)
            for ps in person_sedes:
                ps.DeleteAt = timezone.now()
                ps.save()
        self.stdout.write(self.style.SUCCESS(f'{total} instructores desactivados por contrato vencido.'))

# comanndo para desactivar instructores vencidos
# python manage.py desactivar_instructores_vencidos