USE bdautogestion;
SET FOREIGN_KEY_CHECKS = 0;

-- Limpiar datos existentes
DELETE FROM `security_rolformpermission`;
DELETE FROM `security_formmodule`;
DELETE FROM `security_form`;
DELETE FROM `security_module`;
DELETE FROM `security_permission`;
DELETE FROM `security_role`;
DELETE FROM `general_aprendiz`;
DELETE FROM `general_instructor`;
DELETE FROM `general_ficha`;
DELETE FROM `general_program`;
DELETE FROM `general_knowledgearea`;
DELETE FROM `general_personsede`;
DELETE FROM `general_sede`;
DELETE FROM `general_center`;
DELETE FROM `general_regional`;

-- Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- ==================================================
-- DATOS GENERALES
-- ==================================================

-- Insertar datos en general_regional
INSERT INTO `general_regional` VALUES 
(1,'Huila',75001,'Regional Huila',1,'Calle 21 # 8-80, Neiva, Huila',NULL);

-- Insertar datos en general_center
INSERT INTO `general_center` VALUES 
(1,'Centro de la industria la empresa y los servicios',9570001,'Calle 21 # 8-80, Neiva',1,NULL,1);

-- Insertar datos en general_sede
INSERT INTO `general_sede` VALUES 
(1,'Sede Comercio y servicios',957001,'Calle 5 # 12-34','8871234','comercio@sena.edu.co',1,NULL,1),
(2,'Sede Industrial',957002,'Calle 26 # 15-67','8875678','industrial@sena.edu.co',1,NULL,1);

-- Insertar datos en general_knowledgearea
INSERT INTO `general_knowledgearea` VALUES 
(1,'Diseño','Área especializada en diseño gráfico y multimedia',1,NULL),
(2,'Tecnología','Área de desarrollo de software y tecnologías de la información',1,NULL),
(3,'Administración','Área de gestión empresarial y administrativa',1,NULL);

-- Insertar datos en general_program
INSERT INTO `general_program` VALUES 
(1,228106,'Análisis y Desarrollo de Software','Tecnólogo','Programa de formación en desarrollo de software',1,NULL),
(2,224002,'Diseño Gráfico','Técnico','Programa de formación en diseño gráfico',1,NULL),
(3,122331,'Gestión Empresarial','Tecnólogo','Programa de formación en administración de empresas',1,NULL);

-- Insertar datos en general_ficha
INSERT INTO `general_ficha` VALUES 
(1,2901817,1,NULL,1),
(2,2901885,1,NULL,2),
(3,2901920,1,NULL,3);

-- ==================================================
-- DATOS DE SEGURIDAD
-- ==================================================

-- Insertar datos en security_module
INSERT INTO `security_module` VALUES 
(1,'Dashboard','Módulo principal del sistema con estadísticas y resúmenes',1,NULL),
(2,'Seguridad','Módulo de administración de usuarios, roles y permisos',1,NULL),
(3,'Gestión Académica','Módulo para gestión de fichas, programas y aprendices',1,NULL),
(4,'Seguimientos','Módulo para asignación y seguimiento de instructores',1,NULL),
(5,'Empresas','Módulo para gestión de empresas y solicitudes',1,NULL);

-- Insertar datos en security_form
INSERT INTO `security_form` VALUES 
(1,'Administración de Usuarios','/admin/users','Gestión completa de usuarios del sistema',1,NULL),
(2,'Gestión de Roles','/admin/roles','Administración de roles y permisos',1,NULL),
(3,'Dashboard Principal','/dashboard','Página principal con estadísticas',1,NULL),
(4,'Registro Masivo','/admin/mass-registration','Registro masivo de usuarios mediante Excel',1,NULL),
(5,'Gestión de Fichas','/academic/fichas','Administración de fichas de formación',1,NULL),
(6,'Gestión de Programas','/academic/programs','Administración de programas de formación',1,NULL),
(7,'Solicitudes de Asignación','/assignments/requests','Gestión de solicitudes de asignación',1,NULL),
(8,'Seguimientos','/assignments/follow-ups','Gestión de seguimientos de etapa práctica',1,NULL),
(9,'Gestión de Empresas','/companies/management','Administración de empresas',1,NULL),
(10,'Mi Perfil','/profile','Gestión del perfil personal',1,NULL);

-- Insertar datos en security_permission
INSERT INTO `security_permission` VALUES 
(1,'Ver','Permiso para visualizar información'),
(2,'Crear','Permiso para crear nuevos registros'),
(3,'Editar','Permiso para modificar registros existentes'),
(4,'Eliminar','Permiso para eliminar registros'),
(5,'Activar/Desactivar','Permiso para cambiar el estado de registros'),
(6,'Exportar','Permiso para exportar datos'),
(7,'Importar','Permiso para importar datos masivamente');

-- Insertar datos en security_role
INSERT INTO `security_role` VALUES 
(1,'Administrador','Acceso total al sistema con todos los permisos',1,NULL),
(2,'Aprendiz','Usuario con acceso limitado para gestionar su etapa práctica',1,NULL),
(3,'Instructor','Usuario con permisos para realizar seguimientos',1,NULL),
(4,'Coordinador','Usuario con permisos de coordinación académica',1,NULL);

-- ==================================================
-- RELACIONES (TABLAS CON DEPENDENCIAS)
-- ==================================================

-- Insertar datos en security_formmodule (relaciona formularios con módulos)
INSERT INTO `security_formmodule` VALUES 
(1,1,2),  -- Administración de Usuarios -> Seguridad
(2,2,2),  -- Gestión de Roles -> Seguridad
(3,3,1),  -- Dashboard Principal -> Dashboard
(4,4,2),  -- Registro Masivo -> Seguridad
(5,5,3),  -- Gestión de Fichas -> Gestión Académica
(6,6,3),  -- Gestión de Programas -> Gestión Académica
(7,7,4),  -- Solicitudes de Asignación -> Seguimientos
(8,8,4),  -- Seguimientos -> Seguimientos
(9,9,5),  -- Gestión de Empresas -> Empresas
(10,10,1); -- Mi Perfil -> Dashboard

-- Insertar datos en security_rolformpermission (permisos por rol y formulario)
-- Formato: (id, form_id, permission_id, role_id)
-- ADMINISTRADOR (rol 1) - Acceso total
INSERT INTO `security_rolformpermission` VALUES 
-- Dashboard Principal (form_id=3, role_id=1)
(1,3,1,1),(2,3,2,1),(3,3,3,1),(4,3,4,1),(5,3,5,1),(6,3,6,1),(7,3,7,1),
-- Administración de Usuarios (form_id=1, role_id=1)
(8,1,1,1),(9,1,2,1),(10,1,3,1),(11,1,4,1),(12,1,5,1),(13,1,6,1),(14,1,7,1),
-- Gestión de Roles (form_id=2, role_id=1)
(15,2,1,1),(16,2,2,1),(17,2,3,1),(18,2,4,1),(19,2,5,1),(20,2,6,1),
-- Registro Masivo (form_id=4, role_id=1)
(21,4,1,1),(22,4,2,1),(23,4,7,1),
-- Gestión de Fichas (form_id=5, role_id=1)
(24,5,1,1),(25,5,2,1),(26,5,3,1),(27,5,4,1),(28,5,5,1),(29,5,6,1),
-- Gestión de Programas (form_id=6, role_id=1)
(30,6,1,1),(31,6,2,1),(32,6,3,1),(33,6,4,1),(34,6,5,1),(35,6,6,1),
-- Solicitudes de Asignación (form_id=7, role_id=1)
(36,7,1,1),(37,7,2,1),(38,7,3,1),(39,7,4,1),(40,7,5,1),(41,7,6,1),
-- Seguimientos (form_id=8, role_id=1)
(42,8,1,1),(43,8,2,1),(44,8,3,1),(45,8,4,1),(46,8,5,1),(47,8,6,1),
-- Gestión de Empresas (form_id=9, role_id=1)
(48,9,1,1),(49,9,2,1),(50,9,3,1),(51,9,4,1),(52,9,5,1),(53,9,6,1),
-- Mi Perfil (form_id=10, role_id=1)
(54,10,1,1),(55,10,3,1);

-- APRENDIZ (rol 2) - Acceso limitado
INSERT INTO `security_rolformpermission` VALUES 
-- Dashboard Principal (form_id=3, role_id=2)
(56,3,1,2),
-- Solicitudes de Asignación (form_id=7, role_id=2) - solo ver y crear
(57,7,1,2),(58,7,2,2),
-- Mi Perfil (form_id=10, role_id=2)
(59,10,1,2),(60,10,3,2);

-- INSTRUCTOR (rol 3) - Acceso a seguimientos
INSERT INTO `security_rolformpermission` VALUES 
-- Dashboard Principal (form_id=3, role_id=3)
(61,3,1,3),
-- Solicitudes de Asignación (form_id=7, role_id=3) - ver y editar
(62,7,1,3),(63,7,3,3),
-- Seguimientos (form_id=8, role_id=3) - completo
(64,8,1,3),(65,8,2,3),(66,8,3,3),(67,8,6,3),
-- Gestión de Empresas (form_id=9, role_id=3) - solo ver
(68,9,1,3),
-- Mi Perfil (form_id=10, role_id=3)
(69,10,1,3),(70,10,3,3);

-- COORDINADOR (rol 4) - Acceso académico amplio
INSERT INTO `security_rolformpermission` VALUES 
-- Dashboard Principal (form_id=3, role_id=4)
(71,3,1,4),(72,3,6,4),
-- Gestión de Fichas (form_id=5, role_id=4)
(73,5,1,4),(74,5,2,4),(75,5,3,4),(76,5,5,4),(77,5,6,4),
-- Gestión de Programas (form_id=6, role_id=4)
(78,6,1,4),(79,6,2,4),(80,6,3,4),(81,6,5,4),(82,6,6,4),
-- Solicitudes de Asignación (form_id=7, role_id=4)
(83,7,1,4),(84,7,3,4),(85,7,5,4),(86,7,6,4),
-- Seguimientos (form_id=8, role_id=4)
(87,8,1,4),(88,8,3,4),(89,8,6,4),
-- Gestión de Empresas (form_id=9, role_id=4)
(90,9,1,4),(91,9,3,4),(92,9,6,4),
-- Mi Perfil (form_id=10, role_id=4)
(93,10,1,4),(94,10,3,4);

-- Script completado exitosamente
SELECT 'Datos configurados correctamente para bdautogestion' as mensaje;
SELECT 'Total de registros insertados:' as info;
SELECT 
    (SELECT COUNT(*) FROM general_regional) as regionales,
    (SELECT COUNT(*) FROM general_center) as centros,
    (SELECT COUNT(*) FROM general_sede) as sedes,
    (SELECT COUNT(*) FROM general_knowledgearea) as areas_conocimiento,
    (SELECT COUNT(*) FROM general_program) as programas,
    (SELECT COUNT(*) FROM general_ficha) as fichas,
    (SELECT COUNT(*) FROM security_module) as modulos,
    (SELECT COUNT(*) FROM security_form) as formularios,
    (SELECT COUNT(*) FROM security_permission) as permisos,
    (SELECT COUNT(*) FROM security_role) as roles,
    (SELECT COUNT(*) FROM security_formmodule) as form_modules,
    (SELECT COUNT(*) FROM security_rolformpermission) as rol_form_permisos;