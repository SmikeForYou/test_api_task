import os
from social.settings.production import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "%5_=+^yqrtb=1h(g(ztq7s6mk$d@fpzd_&52kr*6qx^o=*4^x7"
SUPERADMINS = [("superadmin@email.com", "superadminpassword")]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB", "social_database"),
        "USER": os.getenv("POSTGRES_USER", "social_database"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "social_database"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": int(os.getenv("POSTGRES_PORT", 5432)),
    }
}
