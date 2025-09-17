# Documentación - Sistema de Plantillas Excel para Registro Masivo

## 📋 Resumen

Se ha implementado exitosamente un sistema completo para generar y descargar plantillas de Excel para el registro masivo de instructores y aprendices en el sistema SENA.

## 🚀 Características Implementadas

### Backend (Django)

1. **ExcelTemplateService** (`apps/security/services/ExcelTemplateService.py`)
   - Servicio completo para generar plantillas Excel con datos actualizados de la BD
   - Consulta automática de áreas de conocimiento, programas, fichas, etc.
   - Estilo profesional con campos obligatorios destacados en rojo
   - Hojas auxiliares con datos de referencia
   - Hoja de instrucciones detalladas

2. **ExcelTemplateViewSet** (`apps/security/views/ExcelTemplateViewSet.py`)
   - Endpoints REST para descargar plantillas
   - Documentación automática con Swagger
   - Manejo de errores robusto

### Frontend (React/TypeScript)

1. **ExcelTemplateService** (`src/Api/Services/ExcelTemplate.ts`)
   - Servicio para comunicarse con el backend
   - Manejo de descargas automáticas
   - Gestión de errores

2. **Componente MassRegistration** (actualizado)
   - Integración completa con el backend
   - Indicadores de carga
   - Manejo de errores con alertas

## 🔗 Endpoints Disponibles

### 1. Descargar Plantilla de Instructores
- **URL**: `GET /api/security/excel-templates/instructor-template/`
- **Descripción**: Descarga plantilla Excel para registro masivo de instructores
- **Respuesta**: Archivo Excel (.xlsx)
- **Hojas incluidas**:
  - Instructores (hoja principal)
  - Áreas de Conocimiento
  - Tipos de Contrato
  - Tipos de Identificación
  - Instrucciones

### 2. Descargar Plantilla de Aprendices
- **URL**: `GET /api/security/excel-templates/aprendiz-template/`
- **Descripción**: Descarga plantilla Excel para registro masivo de aprendices
- **Respuesta**: Archivo Excel (.xlsx)
- **Hojas incluidas**:
  - Aprendices (hoja principal)
  - Programas
  - Fichas
  - Tipos de Identificación
  - Instrucciones

### 3. Información de Plantillas
- **URL**: `GET /api/security/excel-templates/template-info/`
- **Descripción**: Obtiene información detallada sobre las plantillas disponibles
- **Respuesta**: JSON con metadatos de las plantillas

## 📊 Estructura de Plantillas

### Plantilla de Instructores
**Campos principales**:
- Primer Nombre* (obligatorio)
- Segundo Nombre
- Primer Apellido* (obligatorio)
- Segundo Apellido
- Tipo Identificación* (obligatorio)
- Número Identificación* (obligatorio)
- Teléfono* (obligatorio)
- Email Institucional* (obligatorio - @sena.edu.co)
- Tipo de Contrato* (obligatorio)
- Fecha Inicio Contrato* (obligatorio - YYYY-MM-DD)
- Fecha Fin Contrato* (obligatorio - YYYY-MM-DD)
- Área de Conocimiento* (obligatorio)
- Contraseña Temporal* (obligatorio)

### Plantilla de Aprendices
**Campos principales**:
- Primer Nombre* (obligatorio)
- Segundo Nombre
- Primer Apellido* (obligatorio)
- Segundo Apellido
- Tipo Identificación* (obligatorio)
- Número Identificación* (obligatorio)
- Teléfono* (obligatorio)
- Email Institucional* (obligatorio - @soy.sena.edu.co)
- Código Programa* (obligatorio)
- Número Ficha* (obligatorio)
- Contraseña Temporal* (obligatorio)

## 🎨 Características del Diseño

- **Campos obligatorios**: Destacados con fondo rojo
- **Campos opcionales**: Fondo azul estándar
- **Listas desplegables**: Validación automática en campos específicos
- **Hojas auxiliares**: Contienen datos actualizados de la BD
- **Instrucciones**: Hoja dedicada con guías detalladas
- **Ejemplos**: Fila de ejemplo con formatos correctos
- **Autoajuste**: Columnas ajustadas automáticamente

## 📋 Listas Desplegables Implementadas

### Plantilla de Instructores
- **Tipo de Identificación** (Columna E): CC, TI, CE, PP, PEP
- **Tipo de Contrato** (Columna I): Planta, Contratista, Temporal, Prestación de Servicios, Cátedra
- **Área de Conocimiento** (Columna L): Datos actualizados de la BD

### Plantilla de Aprendices
- **Tipo de Identificación** (Columna E): CC, TI, CE, PP, PEP
- **Código Programa** (Columna I): Códigos actualizados de la BD
- **Número Ficha** (Columna J): Números de ficha activos de la BD

## 🔧 Configuración Técnica

### Dependencias Agregadas
```txt
openpyxl>=3.1.0
```

### URLs Configuradas
En `apps/security/urls.py`:
```python
router.register(r'excel-templates', ExcelTemplateViewSet, basename='excel-templates')
```

### Frontend API Config
En `src/Api/config/ConfigApi.ts`:
```typescript
excelTemplates: {
  instructorTemplate: `${API_BASE_URL}security/excel-templates/instructor-template/`,
  aprendizTemplate: `${API_BASE_URL}security/excel-templates/aprendiz-template/`,
  templateInfo: `${API_BASE_URL}security/excel-templates/template-info/`,
}
```

## ✅ Pruebas Realizadas

- ✅ Generación exitosa de plantillas de instructores
- ✅ Generación exitosa de plantillas de aprendices
- ✅ Consulta correcta de datos de la BD
- ✅ Formato y estilo de archivos Excel
- ✅ **Listas desplegables funcionando correctamente**
- ✅ **Validación de datos implementada**
- ✅ Integración frontend-backend
- ✅ Manejo de errores
- ✅ Tamaño de archivos: ~8.8KB (incrementó por las validaciones)

## 🚀 Próximos Pasos

1. **Carga de Archivos**: Implementar endpoints para procesar archivos Excel cargados
2. **Validaciones**: Crear validaciones específicas para los datos importados
3. **Reporting**: Sistema de reportes de importación exitosa/errores
4. **Notificaciones**: Emails automáticos tras importaciones masivas

## 📝 Notas Importantes

- Las plantillas consultan datos actualizados de la BD en tiempo real
- Los campos obligatorios están claramente marcados
- Se incluyen instrucciones detalladas en cada plantilla
- El sistema maneja errores graciosamente
- Compatible con formatos .xlsx y .xls