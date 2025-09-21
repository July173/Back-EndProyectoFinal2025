from rest_framework import serializers

class FormPDFSerializer(serializers.Serializer):
    """
    Serializer para cargar únicamente archivos PDF
    """
    pdf_file = serializers.FileField(help_text="Archivo PDF de la solicitud")
    
    def validate_pdf_file(self, value):
        """Validar que el archivo sea PDF y tenga un tamaño apropiado"""
        if value:
            # Validar extensión
            if not value.name.lower().endswith('.pdf'):
                raise serializers.ValidationError("El archivo debe ser un PDF (.pdf)")
            
            # Validar tamaño (10MB máximo)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("El archivo PDF no puede ser mayor a 10MB")
        
        return value
