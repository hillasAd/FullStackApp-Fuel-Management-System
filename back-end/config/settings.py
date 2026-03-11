from pathlib import Path
import os
import environ
from datetime import timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==============Importacao do ENV===================
env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

ENVIRONMENT = env("ENVIRONMENT", default="dev")

if ENVIRONMENT == "prod":
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

elif ENVIRONMENT == "dev":
    INTERNAL_IPS = ["127.0.0.1"]

elif ENVIRONMENT == "test":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),
        }
    }


DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

if not SECRET_KEY:
    raise Exception("SECRET_KEY não definida")


ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

EMAIL_BACKEND = env("EMAIL_BACKEND")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_FILE_PATH = env("EMAIL_FILE_PATH")

DATABASES = {
    "default": env.db()
}

# ==============================================================================

from shared.logging.logging_config import configure_logging

configure_logging()
# ==============================================================================
AUTH_USER_MODEL = 'authentication.User'

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',  # necessário para logout

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    
    "modules.authentication.apps.AuthenticationConfig",
    "modules.notifications.apps.NotificationsConfig",
    "modules.fuel.apps.FuelConfig",
    "modules.fuelv2.apps.FuelV2Config",
    "shared",
    "modules.dashboard"
]

MIGRATION_MODULES = {
    'authentication': 'modules.authentication.infrastructure.migrations',
    'fuel': 'modules.fuel.infrastructure.migrations',
    'fuelv2': 'modules.fuelv2.infrastructure.migrations',
}


REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "EXCEPTION_HANDLER": "shared.exceptions.exception_handler.custom_exception_handler",
    
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',   # Para quem não está logado (IP)
        'rest_framework.throttling.UserRateThrottle',   # Para quem está logado (User ID)
    ],
     'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',     # IPs desconhecidos: 100 pedidos por dia
        'user': '1000/day',    # Utilizadores logados: 1000 pedidos por dia
        'burst': '60/minute',  # Para evitar "rajadas" (pico de 1 por segundo)
        'sensitive': '5/minute' # Para Login e Operações Críticas
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15  # Quantidade padrão por página
    
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("JWT_ACCESS_LIFETIME")),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("JWT_REFRESH_LIFETIME")),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


MIDDLEWARE = [
    # 1. Segurança de Fronteira (CORS deve ser o primeiro de todos)
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',

    # 2. Sessão e Comunicação Comum
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # 3. Identificação (Essencial para saber QUEM enviou a chave de idempotência)
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # 4. Idempotência e Observabilidade
    'shared.middleware.correlation_id.CorrelationIdMiddleware',

    # 5. Defesa Final
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Para desenvolvimento rápido, usamos a memória local em produção, usaremos Redis.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# A URL permitida para frontend
CORS_ALLOWED_ORIGINS =  env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:5173'])

# Permitir os Headers customizados criados (Correlation-ID)
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-correlation-id", # Para rastrear logs
    "x-idempotency-key", #Para garantir a gestao de concorrencia
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
