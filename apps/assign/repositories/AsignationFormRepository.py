from apps.assign.entity.models import ModalityProductiveStage, RequestAsignation, Enterprise, Boss, HumanTalent
from apps.general.entity.models import Aprendiz

class AsignationFormRepository:
	@staticmethod
	def create_form(validated_data):
		"""
		Crea el formulario de asignación y vincula todas las relaciones usando los IDs recibidos.
		"""
		# Regional, centro, sede
		from apps.general.entity.models import Regional, Center, Sede, Program, Ficha, Instructor
		regional = Regional.objects.get(pk=validated_data['regional_id'])
		center = Center.objects.get(pk=validated_data['training_center_id'])
		sede = Sede.objects.get(pk=validated_data['training_site_id'])

		# Aprendiz y ficha
		apprentice = Aprendiz.objects.get(pk=validated_data['apprentice_id'])
		program = Program.objects.get(pk=validated_data['program_id'])
		ficha = Ficha.objects.get(file_number=validated_data['record_number'])

		# Empresa, jefe, talento humano
		enterprise = Enterprise.objects.get(pk=validated_data['enterprise_id'])
		boss = Boss.objects.get(pk=validated_data['boss_id'])
		human_talent = HumanTalent.objects.get(pk=validated_data['human_talent_id'])

		# Modalidad productiva
		modality = ModalityProductiveStage.objects.get(pk=validated_data['contract_type_id'])

		# Instructor (si aplica, aquí solo ejemplo)
		# instructor = Instructor.objects.get(pk=validated_data.get('instructor_id'))

		# Crear RequestAsignation
		request_asignation = RequestAsignation.objects.create(
			aprendiz=apprentice,
			enterprise=enterprise,
			modality_productive_stage=modality,
			request_date=validated_data.get('contract_start_date'),
			date_start_production_stage=validated_data.get('contract_start_date'),
			pdf_request=validated_data.get('pdf_request'),
			request_state='Pendiente',
		)

		# Crear AsignationInstructor (si aplica)
		# asignation_instructor = AsignationInstructor.objects.create(
		#     instructor=instructor,
		#     request_asignation=request_asignation,
		#     date_asignation=validated_data.get('contract_start_date'),
		# )

		# Actualizar datos relacionados (ejemplo para Aprendiz, Empresa, Boss, HumanTalent)
		# Puedes expandir para actualizar los datos de cada modelo según los datos recibidos
		# Ejemplo:
		# apprentice.person.nombre = validated_data['first_name']
		# apprentice.person.primer_apellido = validated_data['last_name']
		# apprentice.person.segundo_apellido = validated_data['second_last_name']
		# apprentice.person.save()

		# enterprise.name_enterprise = validated_data['enterprise_address']
		# enterprise.nit_enterprise = validated_data['enterprise_nit']
		# enterprise.email_enterprise = validated_data['enterprise_email']
		# enterprise.save()

		# boss.name_boss = validated_data['boss_name']
		# boss.phone_number = validated_data['boss_phone']
		# boss.email_boss = validated_data['boss_email']
		# boss.position = validated_data['boss_position']
		# boss.save()

		# human_talent.name = validated_data['human_talent_name']
		# human_talent.phone_number = validated_data['human_talent_phone']
		# human_talent.email = validated_data['human_talent_email']
		# human_talent.save()

		return request_asignation
