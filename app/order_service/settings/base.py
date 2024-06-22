from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = config("DEBUG") == "True"
SECRET_KEY = config("SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "oauth2_provider",
    "rest_framework",
    "mozilla_django_oidc",
    "drf_spectacular",
    "corsheaders",
    "app.users",
]

AUTHENTICATION_BACKENDS = (
    "app.users.auth.CustomOIDCAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.order_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["app/order_service/"],
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


WSGI_APPLICATION = "app.order_service.wsgi.application"

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


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

SPECTACULAR_AUTO_SCHEMA = True


AUTH_USER_MODEL = "users.User"


OIDC_RP_CLIENT_ID = (
    "698729611020-57975k1mth069l7ms5fu5c5cverg2i49.apps.googleusercontent.com"
)
OIDC_RP_CLIENT_SECRET = "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"

OIDC_OP_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
OIDC_OP_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
OIDC_OP_USER_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
OIDC_OP_JWKS_ENDPOINT = "https://www.googleapis.com/oauth2/v3/certs"

OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = "openid email profile"

SITE_ID = 2
LOGIN_REDIRECT_URL = "/api/v1/auth/callback/"
LOGOUT_REDIRECT_URL = "/"

SPECTACULAR_SETTINGS = {
    "TITLE": "Order API",
    "DESCRIPTION": "Order management service",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
    "SECURITY": [{"Google": ["openid", "email", "profile"]}],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "Google": {
                "type": "oauth2",
                "flows": {
                    "authorizationCode": {
                        "authorizationUrl": OIDC_OP_AUTHORIZATION_ENDPOINT,
                        "tokenUrl": OIDC_OP_TOKEN_ENDPOINT,
                        "scopes": {
                            "openid": "OpenID Connect scope",
                            "email": "Email scope",
                            "profile": "Profile scope",
                        },
                    }
                },
                "x-client-id": OIDC_RP_CLIENT_ID,
                "x-client-secret": OIDC_RP_CLIENT_SECRET,
            }
        }
    },
}


CORS_ALLOW_ALL_ORIGINS = True
