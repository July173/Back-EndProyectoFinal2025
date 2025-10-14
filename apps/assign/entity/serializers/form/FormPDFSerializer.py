from rest_framework import serializers

class FormPDFSerializer(serializers.Serializer):
    """
    Serializer for uploading PDF files only.
    """
    pdf_file = serializers.FileField(help_text="Archivo PDF de la solicitud")  # User-facing help text remains in Spanish

    def validate_pdf_file(self, value):
        """
        Validates that the file is a PDF and has a maximum size of 1MB.
        """
        if value:
            # Validate extension
            if not value.name.lower().endswith('.pdf'):
                raise serializers.ValidationError("El archivo debe ser un PDF (.pdf)")  # User-facing error in Spanish
            # Validate size (max 1MB)
            if value.size > 1024 * 1024:
                raise serializers.ValidationError("El archivo PDF no puede ser mayor a 1MB")  # User-facing error in Spanish
        return value
