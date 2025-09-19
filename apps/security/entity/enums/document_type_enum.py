from enum import Enum

class DocumentType(Enum):
    CC = "Cédula de Ciudadanía"
    TI = "Tarjeta de Identidad"
    CE = "Cédula de Extranjería"
    PASSPORT = "Pasaporte"
    NUMERO_CIEGO_SENA = "Número ciego - SENA"
    DNI = "Documento Nacional de Identificación"
    NIT = "Número de Identificación Tributaria"
    PERMISO_TEMPORAL = "Permiso por Protección Temporal"
