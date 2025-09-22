from rest_framework import serializers

class FormRequestSerializer(serializers.Serializer):
    # IDs para vincular entidades ya existentes
    aprendiz_id = serializers.IntegerField(help_text="ID del aprendiz")
    ficha_id = serializers.IntegerField(help_text="ID de la ficha")

    # Datos que sí se crean en la solicitud
    fecha_inicio_contrato = serializers.DateField(help_text="Fecha de inicio de contrato de aprendizaje")
    fecha_fin_contrato = serializers.DateField(help_text="Fecha de fin de contrato de aprendizaje")
    enterprise_name = serializers.CharField(max_length=100, help_text="Nombre de la empresa")
    enterprise_nit = serializers.IntegerField(help_text="NIT de la empresa (solo números)")
    enterprise_location = serializers.CharField(max_length=255, help_text="Ubicación de la empresa")
    enterprise_email = serializers.EmailField(help_text="Correo electrónico de la empresa")
    boss_name = serializers.CharField(max_length=100, help_text="Nombre del jefe inmediato")
    boss_phone = serializers.IntegerField(help_text="Teléfono del jefe (solo números)")
    boss_email = serializers.EmailField(help_text="Correo del jefe inmediato")
    boss_position = serializers.CharField(max_length=100, help_text="Cargo del jefe inmediato")
    human_talent_name = serializers.CharField(max_length=100, help_text="Nombre del responsable de talento humano")
    human_talent_email = serializers.EmailField(help_text="Correo de talento humano")
    human_talent_phone = serializers.IntegerField(help_text="Teléfono de talento humano (solo números)")
    sede = serializers.IntegerField(help_text="ID de la sede")
    modality_productive_stage = serializers.IntegerField(help_text="ID de la modalidad de etapa productiva")
