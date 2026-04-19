from django.shortcuts import render, get_object_or_404
from django.views import View
from tienda_app.services import CompraRapidaService
from tienda_app.infra.factories import PaymentFactory
from tienda_app.models import Libro
from django.contrib.auth.models import User
from decimal import Decimal


def home(request):
    libros = Libro.objects.all()
    return render(request, 'tienda_app/home.html', {'libros': libros})


class CompraRapidaView(View):

    template_name = 'tienda_app/compra_rapida.html'

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraRapidaService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_contexto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        servicio = self.setup_service()

        try:
            usuario = User.objects.first()
            direccion = request.POST.get('direccion', 'Sin dirección')

            total = servicio.procesar_compra(
                usuario=usuario,
                productos=[libro],
                direccion=direccion,
            )

            return render(request, self.template_name, {
                'mensaje_exito': f'Compra exitosa. Total: {total}',
                'libro': libro,
                'precio_con_iva': libro.precio * Decimal('1.19'),
            })

        except Exception as e:
            print(f"ERROR VISTA HTML: {e}")
            import traceback
            traceback.print_exc()
            return render(request, self.template_name, {
                'error': str(e),
                'libro': libro,
                'precio_con_iva': libro.precio * Decimal('1.19'),
            })