from django.urls import path
from .views import CompraRapidaView, home  
from tienda_app.api.views import CompraAPIView, listar_productos  

urlpatterns = [
    # HTML (navegador)
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida'),

    # API (JSON)
    path('api/v1/productos/', listar_productos),
    path('api/v2/comprar/', CompraAPIView.as_view(), name='api_comprar'),

    # Home
    path('', home, name='home'),
]