from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.FormRequestRepository import FormRequestRepository
from django.db import transaction
import logging

# Importar modelos necesarios
from apps.security.entity.models.Person import Person
from apps.security.entity.models.User import User
from apps.general.entity.models import Aprendiz, Regional, Center, Sede
from apps.assign.entity.models import Enterprise, ModalityProductiveStage

# Importar validaciones
from core.utils.Validation import is_soy_sena_email

logger = logging.getLogger(__name__)

class FormRequestService(BaseService):
    def __init__(self):
        self.repository = FormRequestRepository()
    
    def create_form_request(self, validated_data):
        """
        Crear solicitud de formulario con validaciones integradas.
        Sigue el patrón de AprendizService con validaciones dentro del método principal.
        """
        logger.info(f"Iniciando creación de solicitud para {validated_data.get('person_first_name')} {validated_data.get('person_first_last_name')} {validated_data.get('person_second_last_name', '')}")
        
        # VALIDACIONES DE NEGOCIO (integradas en el método principal)
        
        # Validar confirmación de correo electrónico
        if validated_data['person_email'] != validated_data['confirmar_correo']:
            raise ValueError("Los correos electrónicos no coinciden. El correo y la confirmación de correo deben ser idénticos.")
        
        # Validar que el correo del aprendiz/persona sea de dominio SENA
        if not is_soy_sena_email(validated_data['person_email']):
            raise ValueError("El correo del aprendiz debe terminar en @soy.sena.edu.co")
        
        # Validar que el email no esté ya registrado en el sistema
        if User.objects.filter(email=validated_data['person_email']).exists():
            raise ValueError(f"El correo {validated_data['person_email']} ya está registrado en el sistema.")
        
        # Validar identificación única (Person usa 'number_identification', no 'identification')
        if Person.objects.filter(number_identification=validated_data['person_document_number']).exists():
            raise ValueError(f"La identificación {validated_data['person_document_number']} ya está registrada.")
        
        # Validar NIT único de empresa
        if Enterprise.objects.filter(nit_enterprise=validated_data['enterprise_nit']).exists():
            raise ValueError(f"El NIT {validated_data['enterprise_nit']} ya está registrado para una empresa.")
        
        # Validar email único de empresa
        if Enterprise.objects.filter(email_enterprise=validated_data['enterprise_email']).exists():
            raise ValueError(f"El correo {validated_data['enterprise_email']} ya está registrado para una empresa.")
        
        # Validar que las entidades de referencia existan
        try:
            Regional.objects.get(pk=validated_data['regional'])
            Center.objects.get(pk=validated_data['center'])
            Sede.objects.get(pk=validated_data['sede'])
            ModalityProductiveStage.objects.get(pk=validated_data['modality_productive_stage'])
        except (Regional.DoesNotExist, Center.DoesNotExist, Sede.DoesNotExist, ModalityProductiveStage.DoesNotExist) as e:
            raise ValueError(f"Entidad de referencia no encontrada: {str(e)}")
        
        logger.info("Validaciones de negocio completadas exitosamente")
        
        # TRANSACCIÓN ATÓMICA (patrón AprendizService)
        with transaction.atomic():
            # Delegar creación al repository (solo BD)
            person, aprendiz, enterprise, boss, human_talent, regional, center, sede, modality = self.repository.create_all_dates_form_request(validated_data)
            
            # Construir respuesta (lógica de presentación en service)
            response = {
                'success': True,
                'message': 'Solicitud creada exitosamente',
                'data': {
                    'person': {
                        'id': person.id,
                        'full_name': f"{person.first_name} {person.second_name or ''} {person.first_last_name} {person.second_last_name or ''}".strip(),
                        'phone': person.phone_number,
                        'identification': person.number_identification
                    },
                    'aprendiz': {
                        'id': aprendiz.id,
                        'ficha_id': aprendiz.ficha_id if aprendiz.ficha else None,
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
            for person, aprendiz, enterprise, boss, human_talent in form_requests:
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
