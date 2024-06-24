import os
from pathlib import Path

from decouple import config

DEBUG = config("DEBUG") == "True"
SECRET_KEY = config("SECRET_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = config("DEBUG") == "True"
SECRET_KEY = config("SECRET_KEY")
AFRICASTALKING_USERNAME = config("AFRICASTALKING_USERNAME")
AFRICASTALKING_API_KEY = config("AFRICASTALKING_API_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "rest_framework.authtoken",
    "users",
    "inventory",
    "orders",
    "mozilla_django_oidc",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
]


ROOT_URLCONF = "order_system.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["app/order_system/docs/"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "order_system.wsgi.application"

AUTHENTICATION_BACKENDS = (
    "users.auth.custom_auth_backend.CustomOIDCAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)


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

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SPECTACULAR_AUTO_SCHEMA = True

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"

# okta oidc configs
OKTA_DOMAIN = config("OKTA_DOMAIN")
OIDC_RP_CLIENT_ID = config("OKTA_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = config("OKTA_CLIENT_SECRET")
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_AUTHORIZATION_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/authorize"
OIDC_RP_TOKEN_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/token"
OIDC_OP_USER_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/userinfo"
OIDC_OP_TOKEN_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/token"
OIDC_OP_JWKS_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/keys"
OIDC_OP_TOKEN_REVOKE_ENDPOINT = f"https://{OKTA_DOMAIN}/oauth2/default/v1/revoke"
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 60 * 60
OIDC_STORE_ACCESS_TOKEN = config("OIDC_STORE_ACCESS_TOKEN", True)
OIDC_STORE_ID_TOKEN = config("OIDC_STORE_ID_TOKEN", True)
OIDC_STORE_REFRESH_TOKEN = config("OIDC_STORE_REFRESH_TOKEN", True)
OIDC_RP_SCOPES = config("OIDC_RP_SCOPES", "openid profile email offline_access")
OIDC_EXEMPT_URLS = [
    "oidc_authentication_init",
    "oidc_authentication_callback",
    "logout",
]

SPECTACULAR_SETTINGS = {
    "TITLE": "Savannah Order Management Service.",
    "DESCRIPTION": "A simple order management api",
    "VERSION": "1.0.0",
    "SECURITY": [{"Okta": ["openid", "email", "profile", "offline_access"]}],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "Okta": {
                "type": "oauth2",
                "flows": {
                    "authorizationCode": {
                        "authorizationUrl": OIDC_OP_AUTHORIZATION_ENDPOINT,
                        "tokenUrl": OIDC_OP_TOKEN_ENDPOINT,
                        "scopes": {
                            "openid": "OpenID Connect scope",
                            "email": "Email scope",
                            "profile": "Profile scope",
                            "offline_access": "Offline access scope",
                        },
                    }
                },
            }
        }
    },
}
