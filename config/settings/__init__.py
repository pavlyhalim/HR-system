import os

from .base import *  # noqa: F401, F403

env_name = os.environ.get("DJANGO_ENV", "development")

if env_name == "production":
    from .production import *  # noqa: F401, F403
else:
    from .development import *  # noqa: F401, F403
