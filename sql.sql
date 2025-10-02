USE bdautogestion;
INSERT INTO `general_supportcontact` (`id`, `type`, `label`, `value`, `extra_info`, `active`) VALUES
	(1, 'Email', 'Soporte por correo electrónico', 'servicio@sena.edu.co', 'Respuesta en 24-48 horas', 1),
	(2, 'Teléfono', 'Linea gratuita nacional', '01 8000 910 270', 'Lunes a viernes: 7:00 AM - 7:00 PM', 1),
	(3, 'Enlaces útiles', 'Sofia Plus - Oferta Educativa', 'https://betowa.sena.edu.co/', 'Ninguna', 1);

INSERT INTO `general_supportschedule` (`id`, `day_range`, `hours`, `is_closed`, `notes`) VALUES
	(1, 'Lunes a Viernes', '7:00 AM - 7:00 PM', 0, ''),
	(2, 'Sábados', '8:00 AM - 4:00 PM', 0, ''),
	(3, 'Domingos y festivos', 'ninguna', 1, '');

INSERT INTO `general_typecontract` (`id`, `name`, `description`, `active`, `delete_at`) VALUES
	(1, 'Planta', 'Es un contrato estable y permanente, con todos los beneficios laborales de ley.', 1, NULL),
	(2, 'Contrato', 'Es un acuerdo laboral formal que puede ser por tiempo definido o indefinido, según lo pactado.', 1, NULL),
	(3, 'OPS', 'Significa Orden de Prestación de Servicios, se usa mucho en el sector público. No genera relación laboral ni prestaciones sociales, solo el pago por el servicio prestado.', 1, NULL),
	(4, 'Provisional', 'Es un contrato temporal en un cargo mientras se adelanta un concurso o proceso de selección definitivo.', 1, NULL),
	(5, 'Temporal', 'Es una vinculación por un periodo limitado para cubrir una necesidad específica de la empresa o institución.', 1, NULL),
	(6, 'Prestación de Servicios', 'Es un contrato civil o comercial, donde se paga por realizar una actividad, sin subordinación ni prestaciones sociales.', 1, NULL);

INSERT INTO `general_typeofqueries` (`id`, `name`, `description`, `active`) VALUES
	(1, 'Soporte Técnico', 'Para consultas técnicas del sistema', 1),
	(2, 'Consulta Académica', 'Para consultas académicas del sistema', 1),
	(3, 'Problemas con las plataforma', 'Para consulta sobre problemas con el sistema', 1),
	(4, 'Otros', 'Para consulta sobre el sistema', 1);

INSERT INTO `security_documenttype` (`id`, `name`, `acronyms`, `active`, `delete_at`) VALUES
	(1, 'Cédula de Ciudadanía', 'CC', 1, NULL),
	(2, 'Tarjeta de Identidad', 'TI', 1, NULL),
	(3, 'Cédula de Extranjería', 'CE', 1, NULL),
	(4, 'Pasaporte', 'PASSPORT', 1, NULL),
	(5, 'Número ciego - SENA', 'NUMERO_CIEGO_SENA', 1, NULL),
	(6, 'Documento Nacional de Identificación', 'DNI', 1, NULL),
	(7, 'Número de Identificación Tributaria', 'NIT', 1, NULL),
	(8, 'Permiso por Protección Temporal', 'PERMISO_TEMPORAL', 1, NULL);


INSERT INTO general_regional (name, codeRegional, description, active, address) VALUES
('Distrito Capital', '001', 'Regional que atiende Bogotá D.C. con formación técnica y tecnológica especializada', true, 'Calle 57 No. 8-69, Bogotá D.C.'),
('Antioquia', '002', 'Regional de Antioquia enfocada en industria, servicios y desarrollo empresarial', true, 'Calle 52 No. 48-30, Medellín, Antioquia'),
('Valle del Cauca', '003', 'Regional del Valle especializada en agroindustria y servicios portuarios', true, 'Carrera 15 No. 14-50, Cali, Valle del Cauca'),
('Atlántico', '004', 'Regional del Atlántico con énfasis en logística portuaria y comercio exterior', true, 'Carrera 46 No. 85-35, Barranquilla, Atlántico'),
('Santander', '005', 'Regional de Santander especializada en petróleo, gas y energías renovables', true, 'Carrera 21 No. 37-52, Bucaramanga, Santander'),
('Cundinamarca', '006', 'Regional de Cundinamarca con programas agropecuarios y turísticos', true, 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca'),
('Huila', '007', 'Regional del Huila con programas en café, turismo y energías renovables', true, 'Carrera 5 No. 8-45, Neiva, Huila'),
('Norte de Santander', '008', 'Regional Norte de Santander con programas fronterizos y comercio internacional', true, 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander'),
('Bolívar', '009', 'Regional de Bolívar con énfasis en turismo, logística y servicios portuarios', true, 'Calle 30 No. 17-25, Cartagena, Bolívar'),
('Meta', '010', 'Regional del Meta enfocada en ganadería, agricultura y petróleo', true, 'Calle 32 No. 28-15, Villavicencio, Meta');

INSERT INTO general_center (name, codeCenter, address, active, regional_id) VALUES
('Centro de Biotecnología Agropecuaria', '001001', 'Calle 166 No. 52-05, Bogotá D.C.', true, 1),
('Centro de Diseño y Metrología', '001002', 'Calle 52 No. 13-65, Bogotá D.C.', true, 1),
('Centro de Electricidad y Automatización Industrial', '001003', 'Calle 57 No. 8-69, Bogotá D.C.', true, 1),
('Centro de Gestión de Mercados, Logística y TIC', '001004', 'Carrera 30 No. 17-52, Bogotá D.C.', true, 1),
('Centro de Servicios y Gestión Empresarial', '002001', 'Calle 52 No. 48-30, Medellín, Antioquia', true, 2),
('Centro de Tecnología de la Manufactura Avanzada', '002002', 'Carrera 75 No. 42-169, Medellín, Antioquia', true, 2),
('Centro Minero', '002003', 'Carrera 80 No. 65-223, Medellín, Antioquia', true, 2),
('Centro de Gestión Tecnológica de Servicios', '003001', 'Carrera 15 No. 14-50, Cali, Valle del Cauca', true, 3),
('Centro de Biotecnología Industrial', '003002', 'Carrera 52 No. 2 Bis-15, Cali, Valle del Cauca', true, 3),
('Centro Agropecuario de Buga', '003003', 'Carrera 18 No. 2-24, Buga, Valle del Cauca', true, 3),
('Centro Industrial y de Aviación', '004001', 'Carrera 46 No. 85-35, Barranquilla, Atlántico', true, 4),
('Centro de Comercio y Servicios', '004002', 'Calle 30 No. 15-20, Barranquilla, Atlántico', true, 4),
('Centro de Tecnologías del Gas y Petróleo', '005001', 'Carrera 21 No. 37-52, Bucaramanga, Santander', true, 5),
('Centro de Gestión Industrial', '005002', 'Calle 35 No. 8-43, Bucaramanga, Santander', true, 5),
('Centro Agropecuario y de Biotecnología El Porvenir', '005003', 'Km 13 Vía Rionegro, Rionegro, Santander', true, 5),
('Centro de Desarrollo Agroempresarial', '006001', 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca', true, 6),
('Centro de Gestión y Fortalecimiento Socioempresarial', '006002', 'Carrera 7 No. 12-45, Fusagasugá, Cundinamarca', true, 6),
('Centro de la Industria, la Empresa y los Servicios', '007001', 'Carrera 5 No. 8-45, Neiva, Huila', true, 7),
('Centro Agropecuario La Granja', '007002', 'Km 7 Vía Neiva-Espinal, Neiva, Huila', true, 7),
('Centro de Desarrollo Agroindustrial y Empresarial', '007003', 'Carrera 4 No. 8-15, Pitalito, Huila', true, 7),
('Centro de la Industria Petrolera', '008001', 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander', true, 8),
('Centro Agropecuario La Granja', '008002', 'Carrera 11 No. 10-45, Ocaña, Norte de Santander', true, 8),
('Centro Náutico Pesquero', '009001', 'Calle 30 No. 17-25, Cartagena, Bolívar', true, 9),
('Centro de Industria y Construcción', '009002', 'Zona Industrial Mamonal, Cartagena, Bolívar', true, 9),
('Centro de la Macarena', '010001', 'Calle 32 No. 28-15, Villavicencio, Meta', true, 10),
('Centro Agropecuario La Macarena', '010002', 'Carrera 11 No. 15-30, Villavicencio, Meta', true, 10);

INSERT INTO general_sede (name, codeSede, address, phoneSede, emailContact, active, center_id) VALUES
('Sede Principal Biotecnología', '001001001', 'Calle 166 No. 52-05, Bogotá D.C.', '601-5461500', 'biotecnologia@sena.edu.co', true, 1),
('Sede Ricaurte', '001001002', 'Carrera 13 No. 65-10, Bogotá D.C.', '601-5461501', 'ricaurte@sena.edu.co', true, 1),
('Sede Principal Diseño', '001002001', 'Calle 52 No. 13-65, Bogotá D.C.', '601-5461500', 'diseno@sena.edu.co', true, 2),
('Sede Restrepo', '001002002', 'Calle 20 Sur No. 12-30, Bogotá D.C.', '601-5461502', 'restrepo@sena.edu.co', true, 2),
('Sede Principal Electricidad', '001003001', 'Calle 57 No. 8-69, Bogotá D.C.', '601-5461500', 'electricidad@sena.edu.co', true, 3),
('Sede Salitre', '001003002', 'Avenida El Dorado No. 68D-51, Bogotá D.C.', '601-5461503', 'salitre@sena.edu.co', true, 3),
('Sede Principal Mercados', '001004001', 'Carrera 30 No. 17-52, Bogotá D.C.', '601-5461500', 'mercados@sena.edu.co', true, 4),
('Sede Sur', '001004002', 'Carrera 10 No. 15-20 Sur, Bogotá D.C.', '601-5461504', 'mercados.sur@sena.edu.co', true, 4),
('Sede Principal Empresarial', '002001001', 'Calle 52 No. 48-30, Medellín, Antioquia', '604-5190600', 'empresarial.medellin@sena.edu.co', true, 5),
('Sede Itagüí', '002001002', 'Carrera 51 No. 50-20, Itagüí, Antioquia', '604-5190601', 'itagui@sena.edu.co', true, 5),
('Sede Principal Manufactura', '002002001', 'Carrera 75 No. 42-169, Medellín, Antioquia', '604-5190600', 'manufactura.medellin@sena.edu.co', true, 6),
('Sede Copacabana', '002002002', 'Carrera 47 No. 70-85, Copacabana, Antioquia', '604-5190602', 'copacabana@sena.edu.co', true, 6),
('Sede Principal Minero', '002003001', 'Carrera 80 No. 65-223, Medellín, Antioquia', '604-5190600', 'minero.antioquia@sena.edu.co', true, 7),
('Sede Amalfi', '002003002', 'Calle 12 No. 8-45, Amalfi, Antioquia', '604-5190603', 'amalfi@sena.edu.co', true, 7),
('Sede Principal Servicios Cali', '003001001', 'Carrera 15 No. 14-50, Cali, Valle del Cauca', '602-4315800', 'servicios.cali@sena.edu.co', true, 8),
('Sede Norte Cali', '003001002', 'Calle 70 No. 11-50, Cali, Valle del Cauca', '602-4315801', 'norte.cali@sena.edu.co', true, 8),
('Sede Principal Industrial', '003002001', 'Carrera 52 No. 2 Bis-15, Cali, Valle del Cauca', '602-4315800', 'industrial.cali@sena.edu.co', true, 9),
('Sede Yumbo', '003002002', 'Carrera 8 No. 15-30, Yumbo, Valle del Cauca', '602-4315802', 'yumbo@sena.edu.co', true, 9),
('Sede Principal Buga', '003003001', 'Carrera 18 No. 2-24, Buga, Valle del Cauca', '602-4315800', 'buga@sena.edu.co', true, 10),
('Sede Tuluá', '003003002', 'Calle 26 No. 23-12, Tuluá, Valle del Cauca', '602-4315803', 'tulua@sena.edu.co', true, 10),
('Sede Principal Aviación', '004001001', 'Carrera 46 No. 85-35, Barranquilla, Atlántico', '605-3304400', 'aviacion.atlantico@sena.edu.co', true, 11),
('Sede Soledad', '004001002', 'Carrera 21 No. 45-30, Soledad, Atlántico', '605-3304401', 'soledad@sena.edu.co', true, 11),
('Sede Principal Comercio', '004002001', 'Calle 30 No. 15-20, Barranquilla, Atlántico', '605-3304400', 'comercio.atlantico@sena.edu.co', true, 12),
('Sede Malambo', '004002002', 'Carrera 12 No. 8-25, Malambo, Atlántico', '605-3304402', 'malambo@sena.edu.co', true, 12),
('Sede Principal Gas y Petróleo', '005001001', 'Carrera 21 No. 37-52, Bucaramanga, Santander', '607-6910800', 'gas.santander@sena.edu.co', true, 13),
('Sede Barrancabermeja', '005001002', 'Carrera 28 No. 45-15, Barrancabermeja, Santander', '607-6910801', 'barrancabermeja@sena.edu.co', true, 13),
('Sede Principal Industrial', '005002001', 'Calle 35 No. 8-43, Bucaramanga, Santander', '607-6910800', 'industrial.santander@sena.edu.co', true, 14),
('Sede Girón', '005002002', 'Calle 33 No. 25-10, Girón, Santander', '607-6910802', 'giron@sena.edu.co', true, 14),
('Sede Principal El Porvenir', '005003001', 'Km 13 Vía Rionegro, Rionegro, Santander', '607-6910800', 'elporvenir@sena.edu.co', true, 15),
('Sede Principal Agroempresarial', '006001001', 'Calle 8 No. 4-19, Fusagasugá, Cundinamarca', '601-8821200', 'agroempresarial.cundinamarca@sena.edu.co', true, 16),
('Sede Soacha', '006001002', 'Carrera 9 No. 15-21, Soacha, Cundinamarca', '601-8821201', 'soacha@sena.edu.co', true, 16),
('Sede Principal Socioempresarial', '006002001', 'Carrera 7 No. 12-45, Fusagasugá, Cundinamarca', '601-8821200', 'socioempresarial@sena.edu.co', true, 17),
('Sede Girardot', '006002002', 'Calle 17 No. 5-22, Girardot, Cundinamarca', '601-8821202', 'girardot@sena.edu.co', true, 17),
('Sede Principal Neiva', '007001001', 'Carrera 5 No. 8-45, Neiva, Huila', '608-8750400', 'neiva@sena.edu.co', true, 18),
('Sede Centro', '007001002', 'Calle 12 No. 5-30, Neiva, Huila', '608-8750401', 'neiva.centro@sena.edu.co', true, 18),
('Sede La Granja', '007002001', 'Km 7 Vía Neiva-Espinal, Neiva, Huila', '608-8750400', 'lagranja.huila@sena.edu.co', true, 19),
('Sede Campoalegre', '007002002', 'Calle 8 No. 6-15, Campoalegre, Huila', '608-8750402', 'campoalegre@sena.edu.co', true, 19),
('Sede Principal Pitalito', '007003001', 'Carrera 4 No. 8-15, Pitalito, Huila', '608-8750400', 'pitalito@sena.edu.co', true, 20),
('Sede Garzón', '007003002', 'Carrera 6 No. 7-45, Garzón, Huila', '608-8750403', 'garzon@sena.edu.co', true, 20),
('Sede Principal Cúcuta', '008001001', 'Avenida 4 No. 12-52, Cúcuta, Norte de Santander', '607-5820400', 'cucuta@sena.edu.co', true, 21),
('Sede Villa del Rosario', '008001002', 'Carrera 5 No. 8-20, Villa del Rosario, Norte de Santander', '607-5820401', 'villadelrosario@sena.edu.co', true, 21),
('Sede Principal Ocaña', '008002001', 'Carrera 11 No. 10-45, Ocaña, Norte de Santander', '607-5820400', 'ocana@sena.edu.co', true, 22),
('Sede Convención', '008002002', 'Calle 7 No. 9-25, Convención, Norte de Santander', '607-5820402', 'convencion@sena.edu.co', true, 22),
('Sede Principal Náutico', '009001001', 'Calle 30 No. 17-25, Cartagena, Bolívar', '605-6640600', 'nautico.bolivar@sena.edu.co', true, 23),
('Sede Bazurto', '009001002', 'Barrio Bazurto, Cartagena, Bolívar', '605-6640601', 'bazurto@sena.edu.co', true, 23),
('Sede Principal Industrial', '009002001', 'Zona Industrial Mamonal, Cartagena, Bolívar', '605-6640600', 'industrial.bolivar@sena.edu.co', true, 24),
('Sede Magangué', '009002002', 'Calle 15 No. 8-30, Magangué, Bolívar', '605-6640602', 'magangue@sena.edu.co', true, 24),
('Sede Principal Villavicencio', '010001001', 'Calle 32 No. 28-15, Villavicencio, Meta', '608-6620400', 'villavicencio@sena.edu.co', true, 25),
('Sede Kirpas', '010001002', 'Carrera 35 No. 25-40, Villavicencio, Meta', '608-6620401', 'kirpas@sena.edu.co', true, 25),
('Sede Agropecuario Macarena', '010002001', 'Carrera 11 No. 15-30, Villavicencio, Meta', '608-6620400', 'agropecuario.meta@sena.edu.co', true, 26),
('Sede Granada', '010002002', 'Carrera 9 No. 10-15, Granada, Meta', '608-6620402', 'granada@sena.edu.co', true, 26);

INSERT INTO general_knowledgearea VALUES (1,'Diseño','Pertence al area de diseño',1,NULL);

INSERT INTO assign_modalityproductivestage VALUES(1,'Contrato de aprendizaje','El aprendiz desarrolla su etapa practica con contrato de aprendizaje',1,NULL);

INSERT INTO general_program VALUES 
(1,1001,'Análisis y Desarrollo de Software','Tecnologo','Programa de desarrollo',1,NULL),
(2,1002,'Diseño Gráfico','Tecnico','Programa de diseño',1,NULL);

INSERT INTO general_ficha (file_number, program_id, active) VALUES 
(2901817,1,1),
(2901885,2,1);

INSERT INTO security_module VALUES 
(1,'Inicio','Parte inicial del sistema',1,NULL),
(2,'Seguridad','Administra el sistema',1,NULL),
(3,'Asignar seguimientos','Todo lo del proceso de asignar un instructor a un aprendiz para el seguimiento de su etapa practica',1,NULL);


INSERT INTO security_form VALUES
(1,'Administración','Toda la seccion de control de administración del sistema, del modulo de seguridad','/admin',1,NULL),
(2,'Registro Masivo','Toda la seccion de registro de usuarios masivamente mediante plantillas de excel','/mass-registration',1,NULL),
(3,'Inicio','El inicio del sistema','/home',1,NULL),
(4,'Solicitud','solicitud de aprendiz para asignacion de instructor','/request-registration',1,NULL),
(5,'Reasignar','El coordinador reasigna instructor a algun aprendiz','/reassign',1,NULL),
(6,'Seguimiento','El instructor hace seguimiento a los aprendices en su etapa practica','/following',1,NULL),
(7,'Historial de seguimiento','Historial de todos los seguimientos de todos los aprendices','/following-history',1,NULL),
(8,'Evaluar visita final','El coordinador evalua la visita final que suben los instructores','/evaluate-final-visit',1,NULL),
(9,'Asignar','El coordinaro asigna instructor a aprendiz','/assign',1,NULL);

INSERT INTO security_permission VALUES 
(1,'Ver','Visualizar los datos'),
(2,'Editar','Editar los datos'),
(3,'Registrar','ingresar datos nuevos'),
(4,'Eliminar','Eliminar permanentemente datos'),
(5,'Activar','Activar datos');

INSERT INTO security_role VALUES 
(1,'Administrador','Administra y tiene acceso absoluto al sistema',1,NULL),
(2,'Aprendiz','Accede a sus secciones permitidas en el sistema',1,NULL),
(3,'Instructor','Accede a sus secciones permitidas en el sistema',1,NULL),
(4,'Coordinador','El coordinador evalua y sigue los procesos',1,NULL);

INSERT INTO security_formmodule VALUES
(1,1,2),
(2,2,2),
(3,3,1),
(10,4,3),
(11,6,3),
(12,5,3),
(13,7,3),
(14,8,3),
(15,9,3);

INSERT INTO security_rolformpermission VALUES 
(16,3,1,2),(17,3,1,3),(18,4,1,2),(19,4,4,2),(20,2,1,4),(21,2,2,4),(22,2,3,4),(23,2,4,4),(24,2,5,4),(25,3,1,4),(26,3,2,4),(27,3,3,4),(28,3,4,4),(29,3,5,4),(30,5,1,4),(31,5,2,4),(32,5,3,4),(33,5,4,4),(34,5,5,4),(35,7,1,4),(36,7,2,4),(37,7,3,4),(38,7,4,4),(39,7,5,4),(40,8,1,4),(41,8,2,4),(42,8,3,4),(43,8,4,4),(44,8,5,4),(45,9,1,4),(46,9,2,4),(47,9,3,4),(48,9,4,4),(49,9,5,4),(50,3,1,3),(51,6,1,3),(52,6,2,3),(53,6,3,3),(54,6,4,3),(55,6,5,3),(56,7,1,3),(57,7,2,3),(58,7,3,3),(59,7,4,3),(60,7,5,3),(106,1,1,1),(107,1,2,1),(108,1,3,1),(109,1,4,1),(110,1,5,1),(111,1,1,1),(112,1,2,1),(113,1,3,1),(114,1,4,1),(115,1,5,1),(116,2,1,1),(117,2,2,1),(118,2,3,1),(119,2,4,1),(120,2,5,1),(121,2,1,1),(122,2,2,1),(123,2,3,1),(124,2,4,1),(125,2,5,1),(126,3,1,1),(127,3,2,1),(128,3,3,1),(129,3,4,1),(130,3,5,1),(131,3,1,1),(132,3,2,1),(133,3,3,1),(134,3,4,1),(135,3,5,1),(136,5,1,1),(137,5,2,1),(138,5,3,1),(139,5,4,1),(140,5,5,1),(141,7,1,1),(142,7,2,1),(143,7,3,1),(144,7,4,1),(145,7,5,1),(146,8,1,1),(147,8,2,1),(148,8,3,1),(149,8,4,1),(150,8,5,1),(151,9,1,1),(152,9,2,1),(153,9,3,1),(154,9,4,1),(155,9,5,1);

USE bdautogestion;

INSERT INTO `general_legaldocument` (`type`, `title`, `effective_date`, `last_update`, `active`)
VALUES ('terms', 'Términos y condiciones', '2025-10-01', '2025-10-01', 1);

SET @docId = LAST_INSERT_ID();


INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES 
(1, '1', 'Aceptación de los términos',
 'Al acceder y utilizar los servicios del SENA (Servicio Nacional de Aprendizaje), usted acepta estar sujeto a estos términos y condiciones de uso. Si no está de acuerdo con alguno de estos términos, no debe utilizar nuestros servicios. El SENA se reserva el derecho de modificar estos términos en cualquier momento. Las modificaciones entrarán en vigor inmediatamente después de su publicación en este sitio web.',
 1, @docId, NULL);
SET @s1 = LAST_INSERT_ID();

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES 
(2, '2', 'Descripción de los servicios',
 'El SENA ofrece formación profesional integral gratuita en los siguientes servicios:
 - Programas de formación técnica y tecnológica
 - Cursos complementarios virtuales y presenciales
 - Servicios de empleabilidad y emprendimiento
 - Plataformas educativas digitales (Sofia Plus, LMS SENA)
 - Servicios de bienestar al aprendiz
 - Certificación de competencias laborales',
 1, @docId, NULL);
SET @s2 = LAST_INSERT_ID();


INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (3, '3', 'Obligaciones del usuario', NULL, 1, @docId, NULL);
SET @s3 = LAST_INSERT_ID();


INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES 
(1, '3.1', 'Requisitos de registro',
 '- Proporcionar información verdadera, precisa y completa
 - Mantener actualizada su información personal
 - Ser responsables de la confidencialidad de sus credenciales
 - Cumplir con los requisitos académicos establecidos',
 1, @docId, @s3);
SET @s31 = LAST_INSERT_ID();

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES 
(2, '3.2', 'Conducta del usuario',
 '- Respetar las normas de convivencia institucional
 - No utilizar los servicios para fines ilegales o no autorizados
 - Mantener un comportamiento ético y profesional
 - Respetar los derechos de propiedad intelectual
 - No compartir contenido inapropiado o ofensivo',
 1, @docId, @s3);
SET @s32 = LAST_INSERT_ID();


INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES
(4, '4', 'Derechos de propiedad intelectual',
 'Todo el contenido disponible en las plataformas del SENA, incluyendo pero no limitado a textos, gráficos, logotipos, iconos, imágenes, clips de audio, descargas digitales y compilaciones de datos, es propiedad del SENA o de sus proveedores de contenido y está protegido por las leyes de derechos de autor de Colombia e internacionales. Los usuarios pueden utilizar el contenido únicamente para fines educativos personales y no comerciales, respetando siempre los créditos correspondientes.',
 1, @docId, NULL),

(5, '5', 'Protección de datos personales',
 'El SENA se compromete a proteger la privacidad de los usuarios conforme a la Ley 1581 de 2012 y el Decreto 1377 de 2013 sobre Protección de Datos Personales en Colombia. Para más información sobre cómo recopilamos, utilizamos y protegemos sus datos personales, consulte nuestra Política de Privacidad.',
 1, @docId, NULL),

(6, '6', 'Limitación de responsabilidad',
 'El SENA no será responsable por daños directos, indirectos, incidentales, especiales o consecuenciales que resulten del uso o la imposibilidad de uso de nuestros servicios. Nos esforzamos por mantener la disponibilidad continua de nuestros servicios, pero no garantizamos que estén libres de interrupciones, errores o virus.',
 1, @docId, NULL),

(7, '7', 'Terminación del servicio',
 'El SENA se reserva el derecho de suspender o terminar el acceso a sus servicios a cualquier usuario que viole estos términos y condiciones, sin previo aviso. Los usuarios pueden solicitar la terminación de su cuenta en cualquier momento contactando a nuestro servicio de soporte.',
 1, @docId, NULL),

(8, '8', 'Ley Aplicable y jurisdicción',
 'Estos términos y condiciones se rigen por las leyes de la República de Colombia. Cualquier disputa que surja en relación con estos términos será sometida a la jurisdicción exclusiva de los tribunales competentes de Bogotá D.C., Colombia.',
 1, @docId, NULL);
USE bdautogestion;

INSERT INTO `general_legaldocument` (`type`, `title`, `effective_date`, `last_update`, `active`)
VALUES ('privacy', 'Política de privacidad', '2025-10-01', '2025-10-01', 1);

SET @docId = LAST_INSERT_ID();

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (1, '1', 'Información que recopilamos', NULL, 1, @docId, NULL);

SET @s1 = LAST_INSERT_ID();

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (1, '1.1', 'Información personal',
'Nombres y apellidos completos
Número de identificación
Fecha de nacimiento
Dirección de residencia
Correo electrónico
Número de teléfono
Información académica y profesional
Estado socioeconómico (cuando aplique)', 
1, @docId, @s1);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (2, '1.2', 'Información técnica',
'Dirección IP
Tipo de navegador y versión
Sistema operativo
Páginas visitadas y tiempo de permanencia
Cookies y tecnologías similares',
1, @docId, @s1);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (2, '2', 'Uso de la información', NULL, 1, @docId, NULL);

SET @s2 = LAST_INSERT_ID();

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (1, '2.1', 'Servicios educativos',
'Gestión de inscripciones y matrículas
Seguimiento académico y evaluación
Emisión de certificados y títulos
Comunicación sobre programas y cursos',
1, @docId, @s2);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (2, '2.2', 'Servicios administrativos',
'Verificación de identidad
Gestión de pagos (cuando aplique)
Soporte técnico y atención al usuario
Cumplimiento de obligaciones legales',
1, @docId, @s2);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (3, '2.3', 'Mejora de servicios',
'Análisis estadístico y de rendimiento
Personalización de la experiencia educativa
Desarrollo de nuevos programas formativos
Investigación educativa institucional',
1, @docId, @s2);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (3, '3', 'Protección de datos', NULL, 1, @docId, NULL);

SET @s3 = LAST_INSERT_ID();

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (1, '3.1', 'Medidas técnicas',
'Cifrado de datos en tránsito y en reposo
Firewalls y sistemas de detección de intrusiones
Copias de seguridad regulares
Actualizaciones de seguridad constantes
Control de acceso basado en roles',
1, @docId, @s3);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (2, '3.2', 'Medidas organizativas',
'Políticas internas de manejo de datos
Capacitación del personal en protección de datos
Procedimientos de respuesta a incidentes
Auditorías regulares de seguridad
Acuerdos de confidencialidad con terceros',
1, @docId, @s3);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (4, '4', 'Derechos sobre los datos',
'Acceso: Conocer qué datos tenemos sobre usted
Rectificación: Corregir datos inexactos o incompletos
Actualización: Mantener sus datos actualizados
Supresión: Solicitar la eliminación de sus datos (cuando sea posible)
Oposición: Oponerse al tratamiento de sus datos en ciertos casos
Portabilidad: Obtener una copia de sus datos en formato estructurado

Para ejercer estos derechos, puede contactarnos a través de los canales indicados al final de esta política.',
1, @docId, NULL);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (5, '5', 'Compartir información', NULL, 1, @docId, NULL);

SET @s5 = LAST_INSERT_ID();

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES 
(1, '5.1', 'Entidades Gubernamentales', 'Con entidades del gobierno colombiano cuando sea requerido por ley o para cumplir con obligaciones regulatorias.', 1, @docId, @s5),
(2, '5.2', 'Proveedores de Servicios', 'Con proveedores de servicios tecnológicos bajo estrictos acuerdos de confidencialidad.', 1, @docId, @s5),
(3, '5.3', 'Instituciones Educativas', 'Con otras instituciones educativas para fines de articulación académica y reconocimiento de estudios.', 1, @docId, @s5),
(4, '5.4', 'Empleadores', 'Con empleadores potenciales, con su consentimiento expreso, para fines de empleabilidad.', 1, @docId, @s5);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (6, '6', 'Retención de datos',
'Datos académicos: permanentes para efectos de certificación
Datos de contacto: mientras mantenga relación activa con el SENA
Datos técnicos: máximo 2 años
Datos financieros: según legislación contable y tributaria',
1, @docId, NULL);

INSERT INTO `general_legalsection` (`order`, `code`, `title`, `content`, `active`, `documentId_id`, `parentId_id`)
VALUES (7, '7', 'Menores de edad',
'Los menores de edad pueden utilizar nuestros servicios con el consentimiento de sus padres o tutores legales. 
Medidas adicionales:
- Verificación del consentimiento parental
- Limitación en la recopilación de datos personales
- Supervisión adicional en el procesamiento de datos
- Derechos especiales de eliminación de datos',
1, @docId, NULL);


SELECT 'Datos insertados correctamente en bdautogestion' as mensaje;