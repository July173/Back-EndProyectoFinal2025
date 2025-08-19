from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================
# CONFIGURACIÓN BÁSICA
# ============================
SECRET_KEY = 'django-insecure-igo_*_$d=s2s+x#u=!whln50*b2(+(9a=3z5rv)tr$v!1h%ty&'
DEBUG = True
ALLOWED_HOSTS = []

# ============================
# APPS INSTALADAS
# ============================
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    # Apps locales
    'apps.security',  # reemplaza 'api' por tu app de seguridad
    'apps.general',  # reemplaza 'general' por tu app general
]

# ============================
# MIDDLEWARE
# ============================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ============================
# BASE DE DATOS (MySQL)
# ============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'bdautogestion',
        'USER': 'root',
        'PASSWORD': 'Paulaarp14#',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}
# ============================
# MODELO DE USUARIO PERSONALIZADO
# ============================
AUTH_USER_MODEL = 'security.User'

# ============================
# VALIDACIÓN DE CONTRASEÑAS
# ============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================
# DJANGO REST FRAMEWORK (DRF)
# ============================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
       # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# Configuración de JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ============================
# SWAGGER / REDOC
# ============================
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': ['get', 'post', 'put', 'delete', 'patch'],
}
REDOC_SETTINGS = {'LAZY_RENDERING': False}

# ============================
# INTERNACIONALIZACIÓN
# ============================
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ============================
# ARCHIVOS ESTÁTICOS
# ============================
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# =============================
# CORS configuration
# ==============================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
     # Backend
    "http://127.0.0.1:8000",
    # Frontend - diferentes puertos comunes
    "http://localhost:3000",    # React/Next.js
    "http://localhost:5173",    # Vite
    "http://localhost:8080",    # Otros dev servers
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173", 
    "http://127.0.0.1:8080",
]

# Email settings
EMAILS_ENABLED = True
EMAILS_FROM_NAME = "AutoGestion SENA"
EMAILS_FROM_EMAIL: str = "bscl20062007@gmail.com"
SMTP_USER: str = "bscl20062007@gmail.com"  # Tu correo completo
SMTP_PASSWORD: str = "giux eley mwzw zape" 
SMTP_HOST: str = "smtp.gmail.com"
SMTP_PORT: int = 587
SMTP_TLS: bool = True
SMTP_SSL: bool = False

EMAIL_RESET_TOKEN_EXPIRE_MINUTES: int = 5
EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 5
FRONTEND_HOST: str = ""
BACKEND_HOST: str = "http://localhost:8000"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bscl20062007@gmail.com'  # Tu correo completo
EMAIL_HOST_PASSWORD = 'giux eley mwzw zape' # Tu contraseña de aplicación de Gmail
DEFAULT_FROM_EMAIL = 'bscl20062007@gmail.com'
