from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models.Person import Person
from apps.general.entity.models import Aprendiz, Regional, Center, Sede
from apps.assign.entity.models import Enterprise, Boss, HumanTalent, ModalityProductiveStage
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class FormRequestRepository(BaseRepository):
    def __init__(self):
        # Repository independiente para manejar FormRequests
        pass
    
    def create_all_dates_form_request(self, data):
        """
        Crea todas las entidades relacionadas con la solicitud de formulario en una sola transacción.
        SOLO maneja comunicación con BD - SIN validaciones de negocio.
        Retorna person, aprendiz, enterprise, boss, human_talent y referencias.
        """
        from django.db import transaction
        with transaction.atomic():
            logger.info(f"Iniciando creación de solicitud para {data.get('person_first_name')} {data.get('person_first_last_name')} {data.get('person_second_last_name', '')}")
            
            # OBTENER ENTIDADES DE REFERENCIA (solo comunicación BD)
            regional = Regional.objects.get(pk=data['regional'])
            center = Center.objects.get(pk=data['center'])
            sede = Sede.objects.get(pk=data['sede'])
            modality = ModalityProductiveStage.objects.get(pk=data['modality_productive_stage'])
            
            # CREACIÓN DE ENTIDADES (solo operaciones BD)
            
            # 1. Crear Person
            # Dividir nombres si vienen en un solo campo
            full_first_name = data['person_first_name'].strip()
            name_parts = full_first_name.split(' ', 1)  # Dividir en máximo 2 partes
            
            first_name = name_parts[0] if name_parts else ''
            second_name = name_parts[1] if len(name_parts) > 1 else ''
            
            person_data = {
                'first_name': first_name,
                'second_name': second_name,  # Segundo nombre extraído automáticamente
                'first_last_name': data['person_first_last_name'],
                'second_last_name': data.get('person_second_last_name', ''),  # Campo opcional
                'phone_number': data['person_phone'],  # Usar phone_number en lugar de phone
                'type_identification': data['person_document_type'],
                'number_identification': data['person_document_number'],  # Usar number_identification
            }
            person = Person.objects.create(**person_data)
            logger.info(f"Persona creada con ID: {person.id}")
            
            # 2. Crear Aprendiz
            aprendiz_data = {
                'person': person,
                'active': True,  # Por defecto activo
            }
            # Solo agregar ficha si se proporciona un ID válido
            if data.get('aprendiz_ficha_id'):
                from apps.general.entity.models import Ficha
                try:
                    ficha = Ficha.objects.get(pk=data.get('aprendiz_ficha_id'))
                    aprendiz_data['ficha'] = ficha
                except Ficha.DoesNotExist:
                    logger.warning(f"Ficha con ID {data.get('aprendiz_ficha_id')} no encontrada")
            
            aprendiz = Aprendiz.objects.create(**aprendiz_data)
            logger.info(f"Aprendiz creado con ID: {aprendiz.id}")
            
            # 3. Crear Enterprise
            enterprise_data = {
                'name_enterprise': data['enterprise_name'],
                'nit_enterprise': data['enterprise_nit'],
                'locate': data['enterprise_location'],
                'email_enterprise': data['enterprise_email'],
            }
            enterprise = Enterprise.objects.create(**enterprise_data)
            logger.info(f"Empresa creada con ID: {enterprise.id}")
            
            # 4. Crear Boss
            boss_data = {
                'enterprise': enterprise,
                'name_boss': data['boss_name'],
                'phone_number': data['boss_phone'],
                'email_boss': data['boss_email'],
                'position': data['boss_position'],
            }
            boss = Boss.objects.create(**boss_data)
            logger.info(f"Jefe creado con ID: {boss.id}")
            
            # 5. Crear HumanTalent
            human_talent_data = {
                'enterprise': enterprise,
                'name': data['human_talent_name'],
                'email': data['human_talent_email'],
                'phone_number': data['human_talent_phone'],
            }
            human_talent = HumanTalent.objects.create(**human_talent_data)
            logger.info(f"Talento humano creado con ID: {human_talent.id}")
            
            logger.info("Solicitud de formulario creada exitosamente")
            
            # Retornar instancias directamente
            return person, aprendiz, enterprise, boss, human_talent, regional, center, sede, modality
    
    def get_all_form_requests(self):
        """
        Obtener todas las solicitudes de formulario con sus relaciones.
        Retorna lista de tuplas con las entidades relacionadas.
        """
        logger.info("Obteniendo todas las solicitudes de formulario")
        
        # Obtener todos los aprendices con sus relaciones optimizadas
        aprendices = Aprendiz.objects.select_related(
            'person'
        ).all()
        
        # Lista para almacenar las solicitudes encontradas
        form_requests = []
        
        for aprendiz in aprendices:
            # Para cada aprendiz, buscar si tiene empresas relacionadas
            # (esto simula una relación implícita ya que no hay tabla de unión directa)
            enterprises = Enterprise.objects.prefetch_related(
                'boss_set',
                'humantalent_set'
            ).all()
            
            for enterprise in enterprises:
                bosses = enterprise.boss_set.all()
                human_talents = enterprise.humantalent_set.all()
                
                # Si la empresa tiene boss y human talent, la consideramos parte de una solicitud
                if bosses.exists() and human_talents.exists():
                    # Crear tupla con las entidades relacionadas (patrón similar a AprendizRepository)
                    form_request = (
                        aprendiz.person,      # Person
                        aprendiz,             # Aprendiz  
                        enterprise,           # Enterprise
                        bosses.first(),       # Boss (tomamos el primero)
                        human_talents.first() # HumanTalent (tomamos el primero)
                    )
                    form_requests.append(form_request)
        
        logger.info(f"Se encontraron {len(form_requests)} solicitudes")
        return form_requests
