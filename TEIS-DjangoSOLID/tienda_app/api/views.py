from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tienda_app.infra.factories import PaymentFactory
from tienda_app.services import CompraRapidaService
from tienda_app.models import Libro, Inventario
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import OrdenInputSerializer

@api_view(['GET'])
def listar_productos(request):
    productos = [
        {"id": 0, "nombre": "Cien años de soledad", "precio": 155.00},
        {"id": 1, "nombre": "Harry Potter y La Orden del Fénix", "precio": 132.00},
        {"id": 2, "nombre": "Clean Code en Python", "precio": 155.00},
        {"id": 3, "nombre": "The Pragmatic Programmer", "precio": 200.00},
        {"id": 4, "nombre": "Refactoring", "precio": 180.00},
    ]
    return Response(productos)

class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/v1/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123"}
    """

    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            # Buscar el libro real en la base de datos
            libro = Libro.objects.get(id=datos['libro_id'])

            # Verificar stock antes de llegar al builder
            inventario = Inventario.objects.get(libro=libro)
            if inventario.cantidad <= 0:
                raise ValueError("No hay existencias disponibles.")

            gateway = PaymentFactory.get_processor()
            servicio = CompraRapidaService(procesador_pago=gateway)

            usuario = request.user if request.user.is_authenticated else None

            # Pasar lista de objetos Libro, no diccionarios
            resultado = servicio.ejecutar_proceso_compra(
                usuario=usuario,
                productos=[libro],
                direccion=datos['direccion_envio'],
            )

            return Response(
                {
                    'estado': 'exito',
                    'mensaje': f'Orden creada. Total: {resultado}',
                },
                status=status.HTTP_201_CREATED,
            )

        except Libro.DoesNotExist:
            return Response({'error': 'Libro no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)