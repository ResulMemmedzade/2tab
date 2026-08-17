import os
import sys
import asyncio

# 1. İlk növbədə settings modulunu təyin edirik
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 2. Django-nu digər bütün Django komponentlərini və routing-i import etməzdən ƏVVƏL işə salırıq
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import messaging.routing 

if sys.platform == 'win32':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            messaging.routing.websocket_urlpatterns
        )
    ),
})