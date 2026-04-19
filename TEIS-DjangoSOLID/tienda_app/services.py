import logging

logger = logging.getLogger(__name__)

from decimal import Decimal
from django.shortcuts import get_object_or_404

from .domain.builders import OrdenBuilder
from .models import Inventario, Libro


class CompraRapidaService:

    def __init__(self, procesador_pago):
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()

    def ejecutar_proceso_compra(self, usuario, productos, direccion):

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos(productos)
            .para_envio(direccion)
            .build()
        )

        logger.info(f"Procesando compra para usuario: {usuario}, productos: {productos}, direccion: {direccion}, total: {orden.total}")

        if self.procesador.pagar(orden.total, libro_nombre=orden.libro.titulo):
            logger.info(f"Compra exitosa. Total pagado: {orden.total}")
            return orden.total

        orden.delete()
        logger.error("Error en la pasarela de pagos. Orden eliminada.")
        raise Exception("Error en la pasarela de pagos")

    def procesar_compra(self, usuario, productos, direccion):
        return self.ejecutar_proceso_compra(usuario, productos, direccion)

    def obtener_contexto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = Inventario.objects.filter(libro=libro).first()

        precio_con_iva = libro.precio * Decimal('1.19')

        return {
            'libro': libro,
            'inventario': inventario,
            'precio_con_iva': precio_con_iva,
        }
        
    def ejecutar_compra(self, libro_id, direccion, usuario):
        """
        Método adaptador para la APIView.
        Busca el libro, construye la lista de productos y delega.
        """
        libro = Libro.objects.get(id=libro_id)
        inventario = Inventario.objects.get(libro=libro)

        if inventario.cantidad <= 0:
            raise ValueError("No hay existencias disponibles.")

        return self.ejecutar_proceso_compra(
            usuario=usuario,
            productos=[libro],
            direccion=direccion
        )