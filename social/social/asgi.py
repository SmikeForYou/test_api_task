import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ social }}.settings")

application = get_asgi_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(application, host="0.0.0.0", port=8080, log_level="info")
