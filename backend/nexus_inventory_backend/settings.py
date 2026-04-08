# Django environ
import environ

# Sentry SDK
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import django.db.models.signals
from pathlib import Path
from configurations import Configuration
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))

environ.Env.read_env(BASE_DIR / ".env")


class Base(Configuration):
    """Configuración base común a todos los entornos"""

    SECRET_KEY = env(
        "DJANGO_SECRET_KEY", default="django-insecure-fallback-key-change-in-production"
    )

    DEBUG = True

    ALLOWED_HOSTS: list[str] = ["127.0.0.1", "localhost"]

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "drf_spectacular",
        "drf_spectacular_sidecar",
        "nexus_inventory_backend.db",
        "api",
        "django_filters",
        "corsheaders",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "nexus_inventory_backend.middleware.MetricsMiddleware",
    ]

    CORS_ALLOWED_ORIGINS = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ]

    CORS_ALLOW_HEADERS = list(default_headers) + [
        "authorization",
    ]

    CORS_ALLOW_METHODS = [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ]

    ROOT_URLCONF = "nexus_inventory_backend.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "nexus_inventory_backend.wsgi.application"

    AUTH_USER_MODEL = "db.User"

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    STATIC_URL = "static/"

    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
    ]

    REST_FRAMEWORK = {
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        "DEFAULT_THROTTLE_CLASSES": [
            "rest_framework.throttling.UserRateThrottle",
        ],
        "DEFAULT_THROTTLE_RATES": {
            "user": "10/min",
        },
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
        "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend"
        ],
    }

    SPECTACULAR_SETTINGS = {
        "ENUM_NAME_OVERRIDES": {
            "StateEnum": "nexus_inventory_backend.db.enums.State",
            "OperationStateEnum": "nexus_inventory_backend.db.enums.OperationState",
            "InvoiceStateEnum": "nexus_inventory_backend.db.enums.InvoiceState",
        },
    }

    sentry_sdk.init(
        dsn=env("SENTRY_DSN", default=None),
        environment=env("ENVIRONMENT", default="development"),
        release=env("SENTRY_RELEASE", default=None),
        send_default_pii=False,
        traces_sample_rate=0.1,
        integrations=[
            DjangoIntegration(
                transaction_style="url",
                middleware_spans=True,
                signals_spans=True,
                signals_denylist=[
                    django.db.models.signals.pre_init,
                    django.db.models.signals.post_init,
                ],
                cache_spans=False,
                http_methods_to_capture=(
                    "CONNECT",
                    "DELETE",
                    "GET",
                    "PATCH",
                    "POST",
                    "PUT",
                    "TRACE",
                ),
            ),
        ],
    )

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "{levelname} {asctime} [{name}] {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "app": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    LOW_STOCK_THRESHOLD = env.int("LOW_STOCK_THRESHOLD", default=5)
    DEFAULT_LIMIT = env.int("DEFAULT_LIMIT", default=10)


class Local(Base):
    """Configuración para desarrollo local con SQLite"""

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }


class Docker(Base):
    """Configuración para contenedor con PostgreSQL"""

    DEBUG = False
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DATABASE_NAME", default="nexus_inventory"),
            "USER": env("DATABASE_USERNAME", default="postgres"),
            "PASSWORD": env("DATABASE_PASSWORD", default="postgres"),
            "HOST": env("DATABASE_HOST", default="localhost"),
            "PORT": env.int("DATABASE_PORT", default=5432),
        }
    }
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])
    SECRET_KEY = env("SECRET_KEY", default="no_hack_me_please")


class Production(Docker):
    """Configuración para producción con SSL/TLS"""

    DEBUG = False

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = "HTTP_X_FORWARDED_PROTO,https"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


class Test(Base):
    """Configuración para tests"""

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
