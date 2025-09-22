from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.RequestAsignationRepository import RequestAsignationRepository
from django.db import transaction
import logging

# Importar modelos necesarios
from apps.general.entity.models import Aprendiz, Ficha, Regional, Center, Sede
from apps.assign.entity.models import ModalityProductiveStage

logger = logging.getLogger(__name__)


class RequestAsignationService(BaseService):
    def get_form_request_by_id(self, request_id):
        """
        Obtener una solicitud de formulario por su ID, retornando solo los campos del formulario y el request_state.
        """
        result = self.repository.get_form_request_by_id(request_id)
        if not result:
            return {
                'success': False,
                'message': 'Solicitud no encontrada',
                'data': None,
                'error_type': 'not_found'
            }
        person, aprendiz, enterprise, boss, human_talent, modality, request_asignation, regional, center, sede = result
        request_item = {
            'aprendiz_id': aprendiz.id,
            'ficha_id': aprendiz.ficha_id if aprendiz.ficha else None,
            'fecha_inicio_contrato': request_asignation.date_start_production_stage,
            'fecha_fin_contrato': getattr(request_asignation, 'date_end_production_stage', None),
            'enterprise_name': enterprise.name_enterprise,
            'enterprise_nit': enterprise.nit_enterprise,
            'enterprise_location': enterprise.locate,
            'enterprise_email': enterprise.email_enterprise,
            'boss_name': boss.name_boss,
            'boss_phone': boss.phone_number,
            'boss_email': boss.email_boss,
            'boss_position': boss.position,
            'human_talent_name': human_talent.name,
            'human_talent_email': human_talent.email,
            'human_talent_phone': human_talent.phone_number,
            'regional': regional.id if regional else None,
            'center': center.id if center else None,
            'sede': sede.id if sede else None,
            'modality_productive_stage': modality.id,
            'request_state': request_asignation.request_state
        }
        return {
            'success': True,
            'message': 'Solicitud encontrada',
            'data': request_item
        }
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
            sede = Sede.objects.get(pk=validated_data['sede'])
            ModalityProductiveStage.objects.get(pk=validated_data['modality_productive_stage'])
        except (Sede.DoesNotExist, ModalityProductiveStage.DoesNotExist) as e:
            raise ValueError(f"Entidad de referencia no encontrada: {str(e)}")
        logger.info("Validaciones completadas exitosamente")
        with transaction.atomic():
            aprendiz, ficha, enterprise, boss, human_talent, sede, modality, request_asignation = self.repository.create_all_dates_form_request(validated_data)
            # Guardar la relación en PersonSede
            from apps.general.entity.models import PersonSede
            person = aprendiz.person
            PersonSede.objects.update_or_create(
                PersonId=person,
                defaults={"SedeId": sede}
            )
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
            
            # Procesar datos para respuesta: solo los campos del FormRequestSerializer
            requests_data = []
            for _, aprendiz, enterprise, boss, human_talent, sede, modality, request_asignation in form_requests:
                request_item = {
                    'aprendiz_id': aprendiz.id,
                    'ficha_id': aprendiz.ficha_id if aprendiz.ficha else None,
                    'fecha_inicio_contrato': request_asignation.date_start_production_stage,
                    'fecha_fin_contrato': getattr(request_asignation, 'date_end_production_stage', None),
                    'enterprise_name': enterprise.name_enterprise,
                    'enterprise_nit': enterprise.nit_enterprise,
                    'enterprise_location': enterprise.locate,
                    'enterprise_email': enterprise.email_enterprise,
                    'boss_name': boss.name_boss,
                    'boss_phone': boss.phone_number,
                    'boss_email': boss.email_boss,
                    'boss_position': boss.position,
                    'human_talent_name': human_talent.name,
                    'human_talent_email': human_talent.email,
                    'human_talent_phone': human_talent.phone_number,
                    'sede': sede.id if sede else None,
                    'modality_productive_stage': modality.id,
                    'request_state': request_asignation.request_state
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