"""
Script para probar la generación de plantillas Excel.
Ejecutar desde la carpeta test.
"""

import os
import sys
import django

# Configurar Django - ir al directorio padre donde está el proyecto Django
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Subir un nivel para llegar al directorio del proyecto
sys.path.append(parent_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Importar el servicio
from apps.security.services.ExcelTemplateService import ExcelTemplateService

def test_excel_templates():
    """Prueba la generación de plantillas Excel"""
    service = ExcelTemplateService()
    
    print("🧪 Iniciando pruebas de plantillas Excel...")
    
    try:
        # Probar plantilla de instructores
        print("\n📋 Generando plantilla de instructores...")
        instructor_response = service.generate_instructor_template()
        print(f"✅ Plantilla de instructores generada exitosamente")
        print(f"   - Tipo de contenido: {instructor_response.get('Content-Type', 'No especificado')}")
        print(f"   - Tamaño aproximado: {len(instructor_response.content)} bytes")
        
        # Probar plantilla de aprendices
        print("\n📋 Generando plantilla de aprendices...")
        aprendiz_response = service.generate_aprendiz_template()
        print(f"✅ Plantilla de aprendices generada exitosamente")
        print(f"   - Tipo de contenido: {aprendiz_response.get('Content-Type', 'No especificado')}")
        print(f"   - Tamaño aproximado: {len(aprendiz_response.content)} bytes")
        
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        
        # Verificar datos de la BD
        print("\n🔍 Verificando datos de la base de datos...")
        from apps.general.entity.models import KnowledgeArea, Program, Ficha
        
        knowledge_areas_count = KnowledgeArea.objects.filter(active=True).count()
        programs_count = Program.objects.filter(active=True).count()
        fichas_count = Ficha.objects.filter(active=True).count()
        
        print(f"   - Áreas de conocimiento activas: {knowledge_areas_count}")
        print(f"   - Programas activos: {programs_count}")
        print(f"   - Fichas activas: {fichas_count}")
        
        if knowledge_areas_count > 0 and programs_count > 0 and fichas_count > 0:
            print("✅ La base de datos contiene datos necesarios para las plantillas")
        else:
            print("⚠️  Advertencia: Algunos datos pueden estar faltando en la BD")
            
    except Exception as e:
        print(f"❌ Error durante las pruebas: {str(e)}")
        import traceback
        print(f"Detalles del error:\n{traceback.format_exc()}")

if __name__ == "__main__":
    test_excel_templates()