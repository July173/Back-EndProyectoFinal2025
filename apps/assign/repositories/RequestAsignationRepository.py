from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import RequestAsignation
from apps.assign.entity.enums.request_state_enum import RequestState
from django.db.models import Q
from apps.general.entity.models import PersonSede
from apps.general.entity.models import Apprentice, Sede
from apps.assign.entity.models import Enterprise, Boss, HumanTalent, ModalityProductiveStage, RequestAsignation
from django.db import transaction
from apps.general.entity.models import Ficha
import logging

logger = logging.getLogger(__name__)



# Repository for handling form requests and related entities
class RequestAsignationRepository(BaseRepository):

    def __init__(self):
        # Initialize with the RequestAsignation model
        super().__init__(RequestAsignation)

    def filter_form_requests(self, search=None, request_state=None, program_id=None):
        """
        Filter form requests by search text, state, and program.
        Returns a queryset of matching requests.
        """
        queryset = RequestAsignation.objects.select_related(
            'apprentice__person',
            'apprentice__ficha__program',
            'enterprise',
            'modality_productive_stage'
        ).all()

        # Filter by text (name or document number)
        if search:
            queryset = queryset.filter(
                Q(apprentice__person__first_name__icontains=search) |
                Q(apprentice__person__first_last_name__icontains=search) |
                Q(apprentice__person__second_last_name__icontains=search) |
                Q(apprentice__person__number_identification__icontains=search)
            )

        # Filter by state
        if request_state:
            queryset = queryset.filter(request_state=request_state)

        # Filter by program
        if program_id:
            queryset = queryset.filter(apprentice__ficha__program_id=program_id)

        return queryset

    
    def get_form_request_by_id(self, request_id):
        """
        Retrieve a form request by its ID, including all related entities.
        Returns a tuple of related objects or None if not found.
        """
        """
        Get a form request by its ID with all related entities.
        """
        try:
            request_asignation = RequestAsignation.objects.select_related(
                'apprentice__person',
                'apprentice__ficha',
                'enterprise',
                'enterprise__boss',
                'enterprise__human_talent',
                'modality_productive_stage'
            ).get(pk=request_id)
            if hasattr(request_asignation.enterprise, 'boss') and hasattr(request_asignation.enterprise, 'human_talent'):
                modality = request_asignation.modality_productive_stage
                regional = getattr(modality, 'regional', None)
                center = getattr(modality, 'center', None)
                sede = getattr(modality, 'sede', None)
                return (
                    request_asignation.apprentice.person,
                    request_asignation.apprentice,
                    request_asignation.enterprise,
                    request_asignation.enterprise.boss,
                    request_asignation.enterprise.human_talent,
                    modality,
                    request_asignation,
                    regional,
                    center,
                    sede
                )
            else:
                return None
        except RequestAsignation.DoesNotExist:
            return None


    def create_all_dates_form_request(self, data):
        """
        Create all related entities for a form request in a single transaction.
        Links the apprentice, updates their record, and creates enterprise, boss, human talent, and the request itself.
        Returns all created/updated instances.
        """
        """
        Creates all related entities for the form request in a single transaction.
        Links the existing apprentice and updates their record.
        """
        
        with transaction.atomic():
            logger.info(f"Iniciando creación de solicitud para {data.get('person_first_name')} {data.get('person_first_last_name')} {data.get('person_second_last_name', '')}")  # User-facing log in Spanish
            
            # Get reference entities (database communication only)
            sede = Sede.objects.get(pk=data['sede'])
            modality = ModalityProductiveStage.objects.get(pk=data['modality_productive_stage'])
            
            # Find existing apprentice
            apprentice = Apprentice.objects.get(pk=data['apprentice_id'])
            
            # Find record and link to apprentice
            ficha = Ficha.objects.get(pk=data['ficha_id'])
            apprentice.ficha = ficha
            apprentice.save()
            
            # Create entities (database operations only)
            
            # Create Enterprise
            enterprise_data = {
                'name_enterprise': data['enterprise_name'],
                'nit_enterprise': data['enterprise_nit'],
                'locate': data['enterprise_location'],
                'email_enterprise': data['enterprise_email'],
            }
            enterprise = Enterprise.objects.create(**enterprise_data)
            logger.info(f"Empresa creada con ID: {enterprise.id}")  # User-facing log in Spanish
            
            # Create Boss
            boss_data = {
                'enterprise': enterprise,
                'name_boss': data['boss_name'],
                'phone_number': data['boss_phone'],
                'email_boss': data['boss_email'],
                'position': data['boss_position'],
            }
            boss = Boss.objects.create(**boss_data)
            logger.info(f"Jefe creado con ID: {boss.id}")  # User-facing log in Spanish
            
            # Create HumanTalent
            human_talent_data = {
                'enterprise': enterprise,
                'name': data['human_talent_name'],
                'email': data['human_talent_email'],
                'phone_number': data['human_talent_phone'],
            }
            human_talent = HumanTalent.objects.create(**human_talent_data)
            logger.info(f"Talento humano creado con ID: {human_talent.id}")  # User-facing log in Spanish
            
            # Create RequestAsignation with PDF
            request_asignation_data = {
                'apprentice': apprentice,
                'enterprise': enterprise,
                'modality_productive_stage': modality,
                'request_date': data['fecha_inicio_contrato'],  # Usar fecha de inicio como fecha de solicitud
                'date_start_production_stage': data['fecha_inicio_contrato'],
                'date_end_production_stage': data['fecha_fin_contrato'],
                'pdf_request': data.get('pdf_request'),  # El archivo PDF
                 'request_state': RequestState.SIN_ASIGNAR,  # Estado inicial correcto del enum
            }
            request_asignation = RequestAsignation.objects.create(**request_asignation_data)
            logger.info(f"RequestAsignation creado con ID: {request_asignation.id}, PDF: {request_asignation.pdf_request}")  # User-facing log in Spanish
            
            logger.info("Solicitud de formulario creada exitosamente")  # User-facing log in Spanish
            
            # Return instances directly (including request_asignation)
            return apprentice, ficha, enterprise, boss, human_talent, sede, modality, request_asignation


    def get_all_form_requests(self):
        """
        Retrieve all form requests with their related entities.
        Returns a list of tuples with all related objects.
        """
        """
        Get all form requests with their related entities. Uses RequestAsignation as the main table connecting everything.
        """
        logger.info("Obteniendo todas las solicitudes de formulario")  # User-facing log in Spanish
        
    # Get all RequestAsignation objects with optimized relationships
        request_asignations = RequestAsignation.objects.select_related(
            'apprentice__person',           # Person a través de Apprentice
            'apprentice__ficha',            # Ficha del apprentice
            'enterprise',                 # Enterprise
            'enterprise__boss',           # Boss (OneToOne)
            'enterprise__human_talent',   # HumanTalent (OneToOne)
            'modality_productive_stage'   # ModalityProductiveStage
        ).all()
        
    # List to store found requests
        form_requests = []

        for request_asignation in request_asignations:
            # Iterate through all requests and collect related entities
            # Check that the enterprise has both boss and human talent
            if hasattr(request_asignation.enterprise, 'boss') and hasattr(request_asignation.enterprise, 'human_talent'):
                modality = request_asignation.modality_productive_stage
                regional = getattr(modality, 'regional', None)
                center = getattr(modality, 'center', None)
                sede = getattr(modality, 'sede', None)
                # Create tuple with related entities
                # Get the location through PersonSede
                person = request_asignation.apprentice.person
                person_sede = PersonSede.objects.filter(PersonId=person).first()
                sede = person_sede.SedeId if person_sede and person_sede.SedeId else None
                form_request = (
                    person,
                    request_asignation.apprentice,
                    request_asignation.enterprise,
                    request_asignation.enterprise.boss,
                    request_asignation.enterprise.human_talent,
                    sede,
                    modality,
                    request_asignation
                )
                form_requests.append(form_request)

        logger.info(f"Se encontraron {len(form_requests)} solicitudes")  # User-facing log in Spanish
        return form_requests
    

    

