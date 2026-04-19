import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def pagar(self, monto: float, libro_nombre: str = "Sin nombre") -> bool:
        archivo_log = "pagos_locales_SARA_HURTADO.log"

        with open(archivo_log, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Transaccion exitosa por: ${monto} - Libro: {libro_nombre}\n")

        return True