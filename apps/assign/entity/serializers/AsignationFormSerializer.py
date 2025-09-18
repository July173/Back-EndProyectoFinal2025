from rest_framework import serializers

class AsignationFormSerializer(serializers.Serializer):
    # Regional, centro de formación y sede
    regional_id = serializers.IntegerField()  # Relación: Regional (FK desde Aprendiz o Centro de formación)
    center_id = serializers.IntegerField()  # Relación: Centro de formación (FK desde Aprendiz)
    sede_id = serializers.IntegerField()  # Relación: Sede centro de formación (FK desde Aprendiz)

    # Aprendiz
    apprentice_id = serializers.IntegerField()  # Relación: Aprendiz (FK desde RequestAsignation)
    program_id = serializers.IntegerField()  # Relación: Programa de formación (FK desde Aprendiz)
    identification_type_id = serializers.IntegerField()  # Relación: Tipo de identificación (FK desde Aprendiz)
    contract_type_id = serializers.IntegerField()  # Relación: Tipo de contrato (FK desde Aprendiz)

    identification_number = serializers.IntegerField()  # Campo directo de Aprendiz
    first_name = serializers.CharField(max_length=100)  # Campo directo de Aprendiz
    last_name = serializers.CharField(max_length=100)  # Campo directo de Aprendiz
    second_last_name = serializers.CharField(max_length=100)  # Campo directo de Aprendiz
    email = serializers.EmailField(max_length=100)  # Campo directo de Aprendiz
    confirm_email = serializers.EmailField(max_length=100)  # Campo directo de Aprendiz
    record_number = serializers.IntegerField()  # Campo directo de Aprendiz
    mobile_phone_number = serializers.IntegerField(max_length=10)  # Campo directo de Aprendiz
    contract_start_date = serializers.DateField()  # Campo directo de RequestAsignation
    contract_end_date = serializers.DateField()  # Campo directo de RequestAsignation

    # Empresa
    enterprise_id = serializers.IntegerField()  # Relación: Empresa (FK desde RequestAsignation)
    enterprise_nit = serializers.IntegerField()  # Campo directo de Empresa
    enterprise_address = serializers.CharField(max_length=255)  # Campo directo de Empresa
    enterprise_email = serializers.EmailField(max_length=100)  # Campo directo de Empresa

    # Jefe inmediato
    boss_id = serializers.IntegerField()  # Relación: Jefe inmediato (FK desde Empresa)
    boss_name = serializers.CharField(max_length=100)  # Campo directo de Boss
    boss_phone = serializers.CharField(max_length=20)  # Campo directo de Boss
    boss_email = serializers.EmailField(max_length=100)  # Campo directo de Boss
    boss_position = serializers.CharField(max_length=100)  # Campo directo de Boss

    # Talento humano
    human_talent_id = serializers.IntegerField()  # Relación: Talento humano (FK desde Empresa)
    human_talent_name = serializers.CharField(max_length=100)  # Campo directo de HumanTalent
    human_talent_phone = serializers.CharField(max_length=20)  # Campo directo de HumanTalent
    human_talent_email = serializers.EmailField(max_length=100)  # Campo directo de HumanTalent

    pdf_request = serializers.FileField(allow_empty_file=False, required=True)  # Archivo PDF de soporte (RequestAsignation)
