USE bdautogestion;

SET FOREIGN_KEY_CHECKS = 0;

-- Limpiar datos existentes
DELETE FROM security_rolformpermission;
DELETE FROM security_formmodule;
DELETE FROM security_form;
DELETE FROM security_module;
DELETE FROM security_permission;
DELETE FROM security_role;
DELETE FROM general_ficha;
DELETE FROM general_program;
DELETE FROM general_knowledgearea;
DELETE FROM general_sede;
DELETE FROM general_center;
DELETE FROM general_regional;

-- Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- Reiniciar AUTO_INCREMENT para las tablas principales
ALTER TABLE security_role AUTO_INCREMENT = 1;
ALTER TABLE security_permission AUTO_INCREMENT = 1;
ALTER TABLE security_form AUTO_INCREMENT = 1;
ALTER TABLE security_module AUTO_INCREMENT = 1;

-- Insertar datos en general_regional
INSERT INTO general_regional VALUES (1,'Huila','REG-HUI','Regional Huila',1,'Neiva',NULL);

-- Insertar datos en general_center
INSERT INTO general_center VALUES (1,'Centro de la industria la empresa y los servicios','CI001','Neiva',1,NULL,1);

-- Insertar datos en general_sede
INSERT INTO general_sede VALUES 
(1,'Sede Comercio y servicios','SC001','Calle 5','8881234','central@sena.edu.co',1,NULL,1),
(2,'Sede industrial','SC002','Calle 26','8885678','cnorte@sena.edu.co',1,NULL,1);

-- Insertar datos en general_knowledgearea
INSERT INTO general_knowledgearea VALUES (1,'Diseño','Pertence al area de diseño',1,NULL);

-- Insertar datos en general_program
INSERT INTO general_program VALUES 
(1,'PROG001','Análisis y Desarrollo de Software','Tecnologo','Programa de desarrollo',1,NULL),
(2,'PROG002','Diseño Gráfico','Tecnico','Programa de diseño',1,NULL);

-- Insertar datos en general_ficha
INSERT INTO general_ficha VALUES 
(1,'2901817',1,NULL,1),
(2,'2901885',1,NULL,2);

-- Insertar datos en security_role
INSERT INTO security_role (id, type_role, description, active) VALUES 
(1,'Administrador','Acceso completo al sistema',1),
(2,'Instructor','Acceso a funciones de instructor',1),
(3,'Aprendiz','Acceso básico como aprendiz',1),
(4,'Coordinador','Coordinador académico',1);

-- Insertar datos en security_permission
INSERT INTO security_permission (id, type_permission, description) VALUES 
(1,'Crear','Permiso para crear registros'),
(2,'Leer','Permiso para leer/consultar registros'),
(3,'Actualizar','Permiso para actualizar registros'),
(4,'Eliminar','Permiso para eliminar registros'),
(5,'Administrar','Permiso completo de administración');

-- Insertar datos en security_module
INSERT INTO security_module VALUES 
(1,'Inicio','Parte inicial del sistema',1,NULL),
(2,'Seguridad','Administra el sistema',1,NULL),
(3,'Asignar seguimientos','Todo lo del proceso de asignar un instructor a un aprendiz para el seguimiento de su etapa practica',1,NULL);

-- Insertar datos en security_form
INSERT INTO security_form VALUES 
(1,'Administración','Toda la seccion de control de administración del sistema, del modulo de seguridad','/admin',1,NULL),
(2,'Registro Masivo','Toda la seccion de registro de usuarios masivamente mediante plantillas de excel','/mass-registration',1,NULL),
(3,'Inicio','El inicio del sistema','/home',1,NULL),
(4,'Solicitud','solicitud de aprendiz para asignacion de instructor','/request-registration',1,NULL);

-- Insertar datos en security_formmodule
INSERT INTO security_formmodule VALUES 
(1,1,2),
(2,2,2),
(3,3,1),
(4,4,3);

-- Insertar datos en security_rolformpermission
-- Formato: (role_id, form_id, permission_id)
INSERT INTO security_rolformpermission (role_id, form_id, permission_id) VALUES 
-- Administrador (role_id=1) - Acceso completo a todos los formularios
(1,1,5),(1,2,5),(1,3,5),(1,4,5),
-- Instructor (role_id=2) - Acceso de lectura y actualización
(2,1,2),(2,2,2),(2,3,2),(2,4,2),
(2,1,3),(2,2,3),(2,3,3),(2,4,3),
-- Aprendiz (role_id=3) - Solo lectura
(3,3,2),(3,4,2),
-- Coordinador (role_id=4) - Permisos específicos
(4,1,2),(4,4,2);

-- Verificar que los datos se insertaron correctamente
SELECT 'Roles insertados:' as info;
SELECT id, type_role, description FROM security_role ORDER BY id;

SELECT 'Permisos insertados:' as info;
SELECT id, type_permission, description FROM security_permission ORDER BY id;