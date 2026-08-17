import os
import sys
import asyncio
from django.core.asgi import get_asgi_application

# 1. Settings modulunu təyin edirik
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 2. Django-nu yükləyirik (bu, arxa planda django.setup() işini görür)
# Bu MÜTLƏQ routing importlarından ƏVVƏL olmalıdır!
django_asgi_app = get_asgi_application()

# 3. Yalnız bundan sonra modellərə ehtiyacı olan routing-i import edirik
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import messaging.routing 

# Windows üçün asyncio tənzimləməsi (Əla əlavədir)
if sys.platform == 'win32':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass

# 4. Tətbiqi qururuq
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # get_asgi_application() əvəzinə yuxarıdakı dəyişəni veririk
    "websocket": AuthMiddlewareStack(
        URLRouter(
            messaging.routing.websocket_urlpatterns
        )
    ),
})