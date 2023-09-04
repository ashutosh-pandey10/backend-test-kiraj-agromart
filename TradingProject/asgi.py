
import os

from uvicorn import run
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TradingProject.settings')

application = get_asgi_application()

if __name__ == "__main__":
    run(application, host="0.0.0.0", port=8000)