# Despliegue con Docker

1. Modifica los valores de usuario, contraseña y nombre de base de datos en `.env` y `docker-compose.yml` si lo deseas.
2. Ejecuta:
   ```powershell
   docker-compose up --build
   ```
3. Accede a la app en [http://localhost:8000](http://localhost:8000)

Recuerda configurar tu `settings.py` para leer las variables de entorno para la base de datos.
