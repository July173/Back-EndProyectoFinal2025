from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.RequestAsignationRepository import RequestAsignationRepository
from django.db import transaction
import logging

# Importar modelos necesarios
from apps.general.entity.models import Aprendiz, Ficha, Regional, Center, Sede
from apps.assign.entity.models import Enterprise, ModalityProductiveStage

logger = logging.getLogger(__name__)


class RequestAsignationService(BaseService):
    def __init__(self):
        self.repository = RequestAsignationRepository()

    def create_form_request(self, validated_data):
        """
        Crear solicitud de formulario con validaciones integradas.
        Vincula aprendiz existente y actualiza su ficha.
        """
        logger.info(f"Iniciando creación de solicitud para aprendiz ID: {validated_data.get('aprendiz_id')}")
        # Validar que el aprendiz y la ficha existan
        try:
            aprendiz = Aprendiz.objects.get(pk=validated_data['aprendiz_id'])
            ficha = Ficha.objects.get(pk=validated_data['ficha_id'])
        except (Aprendiz.DoesNotExist, Ficha.DoesNotExist) as e:
            raise ValueError(f"Entidad no encontrada: {str(e)}")
        # Validar que las entidades de referencia existan
        try:
            Regional.objects.get(pk=validated_data['regional'])
            Center.objects.get(pk=validated_data['center'])
            Sede.objects.get(pk=validated_data['sede'])
            ModalityProductiveStage.objects.get(pk=validated_data['modality_productive_stage'])
        except (Regional.DoesNotExist, Center.DoesNotExist, Sede.DoesNotExist, ModalityProductiveStage.DoesNotExist) as e:
            raise ValueError(f"Entidad de referencia no encontrada: {str(e)}")
        # Se permite repetir el NIT de empresa
        # Validar email único de empresa
        if Enterprise.objects.filter(email_enterprise=validated_data['enterprise_email']).exists():
            raise ValueError(f"El correo {validated_data['enterprise_email']} ya está registrado para una empresa.")
        logger.info("Validaciones completadas exitosamente")
        with transaction.atomic():
            aprendiz, ficha, enterprise, boss, human_talent, regional, center, sede, modality, request_asignation = self.repository.create_all_dates_form_request(validated_data)
            response = {
                'success': True,
                'message': 'Solicitud creada exitosamente',
                'data': {
                    'aprendiz': {
                        'id': aprendiz.id,
                        'ficha_id': ficha.id,
                        'active': aprendiz.active
                    },
                    'enterprise': {
                        'id': enterprise.id,
                        'name': enterprise.name_enterprise,
                        'nit': enterprise.nit_enterprise,
                        'location': enterprise.locate,
                        'email': enterprise.email_enterprise
                    },
                    'boss': {
                        'id': boss.id,
                        'name': boss.name_boss,
                        'phone': boss.phone_number,
                        'email': boss.email_boss,
                        'position': boss.position
                    },
                    'human_talent': {
                        'id': human_talent.id,
                        'name': human_talent.name,
                        'email': human_talent.email,
                        'phone': human_talent.phone_number
                    },
                    'references': {
                        'regional': {'id': regional.id, 'name': regional.name},
                        'center': {'id': center.id, 'name': center.name},
                        'sede': {'id': sede.id, 'name': sede.name},
                        'modality': {'id': modality.id, 'name': modality.name_modality}
                    },
                    'request_asignation': {
                        'id': request_asignation.id,
                        'request_date': request_asignation.request_date,
                        'date_start_production_stage': request_asignation.date_start_production_stage,
                        'date_end_production_stage': getattr(request_asignation, 'date_end_production_stage', None),
                        'request_state': request_asignation.request_state
                    }
                }
            }
            logger.info("Solicitud creada exitosamente")
            return response
    
    def list_form_requests(self):
        """
        Listar solicitudes - solo delega al repository sin validaciones.
        El GET no necesita validaciones de negocio.
        """
        try:
            logger.info("Obteniendo lista de solicitudes")
            
            # Delegar directamente al repository (solo BD)
            form_requests = self.repository.get_all_form_requests()
            
            # Procesar datos para respuesta (lógica de presentación en service)
            requests_data = []
            for person, aprendiz, enterprise, boss, human_talent, modality, request_asignation in form_requests:
                request_item = {
                    'person': {
                        'id': person.id,
                        'full_name': f"{person.first_name} {person.second_name or ''} {person.first_last_name} {person.second_last_name or ''}".strip(),
                        'phone': person.phone_number,
                        'identification': person.number_identification,
                        'document_type': person.type_identification
                    },
                    'aprendiz': {
                        'id': aprendiz.id,
                        'ficha_id': aprendiz.ficha_id if aprendiz.ficha else None,
                        'ficha_name': aprendiz.ficha.name if aprendiz.ficha else None,
                        'active': aprendiz.active
                    },
                    'enterprise': {
                        'id': enterprise.id,
                        'name': enterprise.name_enterprise,
                        'nit': enterprise.nit_enterprise,
                        'location': enterprise.locate,
                        'email': enterprise.email_enterprise
                    },
                    'boss': {
                        'id': boss.id,
                        'name': boss.name_boss,
                        'phone': boss.phone_number,
                        'email': boss.email_boss,
                        'position': boss.position
                    },
                    'human_talent': {
                        'id': human_talent.id,
                        'name': human_talent.name,
                        'email': human_talent.email,
                        'phone': human_talent.phone_number
                    },
                    'modality': {
                        'id': modality.id,
                        'name': modality.name_modality
                    },
                    'request_asignation': {
                        'id': request_asignation.id,
                        'request_date': request_asignation.request_date,
                        'date_start_production_stage': request_asignation.date_start_production_stage,
                        'request_state': request_asignation.request_state,
                        'has_pdf': bool(request_asignation.pdf_request),
                        'pdf_url': request_asignation.pdf_request.url if request_asignation.pdf_request else None
                    }
                }
                requests_data.append(request_item)
            
            logger.info(f"Se encontraron {len(requests_data)} solicitudes")
            return {
                'success': True,
                'message': f'Se encontraron {len(requests_data)} solicitudes',
                'count': len(requests_data),
                'data': requests_data
            }
            
        except Exception as e:
            logger.error(f"Error al listar solicitudes: {str(e)}")
            return {
                'success': False,
                'message': f'Error al obtener las solicitudes: {str(e)}',
                'data': [],
                'error_type': 'database_error'
            }