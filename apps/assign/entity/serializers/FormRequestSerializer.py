from rest_framework import serializers

class FormRequestSerializer(serializers.Serializer):
    # Datos de la persona principal
    person_first_name = serializers.CharField(max_length=100, help_text="Nombres de la persona")
    person_first_last_name = serializers.CharField(max_length=100, help_text="Primer apellido de la persona")
    person_second_last_name = serializers.CharField(max_length=100, required=False, allow_blank=True, help_text="Segundo apellido de la persona")
    person_email = serializers.EmailField(help_text="Correo electrónico de la persona")
    person_phone = serializers.IntegerField(help_text="Número de teléfono (solo números)")
    person_document_type = serializers.CharField(max_length=50, help_text="Tipo de documento (CC, TI, CE, etc.)")
    person_document_number = serializers.CharField(max_length=50, help_text="Número de documento")
    
    # Datos del aprendiz
    aprendiz_ficha_id = serializers.IntegerField(required=False, allow_null=True, help_text="Número de ficha del aprendiz")
    confirmar_correo = serializers.EmailField(help_text="Confirmar correo electrónico")
    fecha_inicio_contrato = serializers.DateField(help_text="Fecha de inicio de contrato de aprendizaje")
    fecha_fin_contrato = serializers.DateField(help_text="Fecha de fin de contrato de aprendizaje")
    
    # Datos de la empresa
    enterprise_name = serializers.CharField(max_length=100, help_text="Nombre de la empresa")
    enterprise_nit = serializers.IntegerField(help_text="NIT de la empresa (solo números)")
    enterprise_location = serializers.CharField(max_length=255, help_text="Ubicación de la empresa")
    enterprise_email = serializers.EmailField(help_text="Correo electrónico de la empresa")
    
    # Datos del jefe inmediato
    boss_name = serializers.CharField(max_length=100, help_text="Nombre del jefe inmediato")
    boss_phone = serializers.IntegerField(help_text="Teléfono del jefe (solo números)")
    boss_email = serializers.EmailField(help_text="Correo del jefe inmediato")
    boss_position = serializers.CharField(max_length=100, help_text="Cargo del jefe inmediato")
    
    # Datos del talento humano
    human_talent_name = serializers.CharField(max_length=100, help_text="Nombre del responsable de talento humano")
    human_talent_email = serializers.EmailField(help_text="Correo de talento humano")
    human_talent_phone = serializers.IntegerField(help_text="Teléfono de talento humano (solo números)")
    
    # Regional, Centro, Sede
    regional = serializers.IntegerField(help_text="ID de la regional")
    center = serializers.IntegerField(help_text="ID del centro")
    sede = serializers.IntegerField(help_text="ID de la sede")
    
    # Modalidad etapa productiva
    modality_productive_stage = serializers.IntegerField(help_text="ID de la modalidad de etapa productiva")
    
    # PDF
    pdf_request = serializers.FileField(required=False, allow_null=True, help_text="Archivo PDF de la solicitud")
