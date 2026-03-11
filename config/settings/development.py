from .base import *  # noqa: F401, F403

DEBUG = True

# Swagger UI sidecar for offline dev
INSTALLED_APPS += ["drf_spectacular_sidecar"]  # noqa: F405

SPECTACULAR_SETTINGS["SWAGGER_UI_DIST"] = "SIDECAR"  # noqa: F405
SPECTACULAR_SETTINGS["SWAGGER_UI_FAVICON_HREF"] = "SIDECAR"  # noqa: F405
