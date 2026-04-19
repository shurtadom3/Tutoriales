from decimal import Decimal
from ..models import Orden, Inventario


class OrdenBuilder:

    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self._items = []
        self._direccion = ""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self

    def con_productos(self, productos):
        self._items = productos
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        if not self._items:
            raise ValueError("Datos insuficientes para crear la orden.")

        subtotal = sum(p.precio for p in self._items)
        total_con_iva = subtotal * Decimal('1.19')

        libro = self._items[0]

        # Descontar inventario
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad <= 0:
            raise ValueError("No hay existencias disponibles.")
        inventario.cantidad -= 1
        inventario.save()

        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=libro,
            total=total_con_iva,
            direccion_envio=self._direccion
        )

        self.reset()
        return orden