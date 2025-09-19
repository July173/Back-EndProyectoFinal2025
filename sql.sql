USE bdautogestion;

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
(4,'Solicitud','solicitud de aprendiz para asignacion de instructor','/request-registration',1,NULL);

INSERT INTO security_permission VALUES 
(1,'Ver','Visualizar los datos'),
(2,'Editar','Editar los datos'),
(3,'Registrar','ingresar datos nuevos'),
(4,'Eliminar','Eliminar permanentemente datos'),
(5,'Activar','Activar datos');

INSERT INTO security_role VALUES 
(1,'Administrador','Administra y tiene acceso absoluto al sistema',1,NULL),
(2,'Aprendiz','Accede a sus secciones permitidas en el sistema',1,NULL),
(3,'Instructor','Accede a sus secciones permitidas en el sistema',1,NULL);

INSERT INTO security_formmodule VALUES 
(1,1,2),
(2,2,2),
(3,3,1),
(4,4,3);

INSERT INTO security_rolformpermission VALUES 
(1,3,1,1),(2,2,1,1),(3,1,1,1),(4,3,2,1),(5,2,2,1),(6,1,2,1),
(7,3,3,1),(8,2,3,1),(9,1,3,1),(10,3,4,1),(11,2,4,1),(12,1,4,1),
(13,3,5,1),(14,2,5,1),(15,1,5,1),(16,3,1,2),(17,3,1,3),(18,4,1,2),(19,4,4,2);

SELECT 'Datos insertados correctamente en bdautogestion' as mensaje;