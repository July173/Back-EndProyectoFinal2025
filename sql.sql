USE bdautogestion;
SET FOREIGN_KEY_CHECKS = 0;

-- Limpiar datos existentes
DELETE FROM `security_rolformpermission`;
DELETE FROM `security_formmodule`;
DELETE FROM `security_form`;
DELETE FROM `security_module`;
DELETE FROM `security_permission`;
DELETE FROM `security_role`;
DELETE FROM `general_ficha`;
DELETE FROM `general_program`;
DELETE FROM `general_knowledgearea`;
DELETE FROM `general_sede`;
DELETE FROM `general_center`;
DELETE FROM `general_regional`;

-- Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- ==================================================
-- DATOS GENERALES
-- ==================================================

-- Insertar datos en general_regional
INSERT INTO `general_regional` VALUES (1,'Huila',1,'Regional Huila',1,'Neiva',NULL);

-- Insertar datos en general_center
INSERT INTO `general_center` VALUES (1,'Centro de la industria la empresa y los servicios',1,'Neiva',1,NULL,1);

-- Insertar datos en general_sede
INSERT INTO `general_sede` VALUES 
(1,'Sede Comercio y servicios',1,'Calle 5','8881234','central@sena.edu.co',1,NULL,1),
(2,'Sede industrial',2,'Calle 26','8885678','cnorte@sena.edu.co',1,NULL,1);

-- Insertar datos en general_knowledgearea
INSERT INTO `general_knowledgearea` VALUES (1,'Diseño','Pertence al area de diseño',1,NULL);

-- Insertar datos en general_program
INSERT INTO `general_program` VALUES 
(1,1001,'Análisis y Desarrollo de Software','Tecnologo','Programa de desarrollo',1,NULL),
(2,1002,'Diseño Gráfico','Tecnico','Programa de diseño',1,NULL);

-- Insertar datos en general_ficha
INSERT INTO `general_ficha` (`file_number`, `program_id`, `active`) VALUES 
(2901817,1,1),
(2901885,2,1);

-- ==================================================
-- DATOS DE SEGURIDAD
-- ==================================================

-- Insertar datos en security_module
INSERT INTO `security_module` VALUES 
(1,'Inicio','Parte inicial del sistema',1,NULL),
(2,'Seguridad','Administra el sistema',1,NULL),
(3,'Asignar seguimientos','Todo lo del proceso de asignar un instructor a un aprendiz para el seguimiento de su etapa practica',1,NULL);

-- Insertar datos en security_form
INSERT INTO `security_form` VALUES 
(1,'Administración','Toda la seccion de control de administración del sistema, del modulo de seguridad','/admin',1,NULL),
(2,'Registro Masivo','Toda la seccion de registro de usuarios masivamente mediante plantillas de excel','/mass-registration',1,NULL),
(3,'Inicio','El inicio del sistema','/home',1,NULL),
(4,'Solicitud','solicitud de aprendiz para asignacion de instructor','/request-registration',1,NULL);

-- Insertar datos en security_permission
INSERT INTO `security_permission` VALUES 
(1,'Ver','Visualizar los datos'),
(2,'Editar','Editar los datos'),
(3,'Registrar','ingresar datos nuevos'),
(4,'Eliminar','Eliminar permanentemente datos'),
(5,'Activar','Activar datos');

-- Insertar datos en security_role
INSERT INTO `security_role` VALUES 
(1,'Administrador','Administra y tiene acceso absoluto al sistema',1,NULL),
(2,'Aprendiz','Accede a sus secciones permitidas en el sistema',1,NULL),
(3,'Instructor','Accede a sus secciones permitidas en el sistema',1,NULL);

-- ==================================================
-- RELACIONES (TABLAS CON DEPENDENCIAS)
-- ==================================================

-- Insertar datos en security_formmodule (depende de security_form y security_module)
INSERT INTO `security_formmodule` VALUES 
(1,1,2),
(2,2,2),
(3,3,1),
(4,4,3);

-- Insertar datos en security_rolformpermission (depende de security_role, security_form, security_permission)
INSERT INTO `security_rolformpermission` VALUES 
(1,3,1,1),(2,2,1,1),(3,1,1,1),(4,3,2,1),(5,2,2,1),(6,1,2,1),
(7,3,3,1),(8,2,3,1),(9,1,3,1),(10,3,4,1),(11,2,4,1),(12,1,4,1),
(13,3,5,1),(14,2,5,1),(15,1,5,1),(16,3,1,2),(17,3,1,3),(18,4,1,2),(19,4,4,2);

-- Script completado exitosamente
SELECT 'Datos insertados correctamente en bdautogestion' as mensaje;