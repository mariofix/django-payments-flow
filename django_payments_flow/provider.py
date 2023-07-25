from typing import Any, Optional

from django.http import JsonResponse
from payments import PaymentError, PaymentStatus, RedirectNeeded
from payments.core import BasicProvider, get_base_url
from payments.forms import PaymentForm as BasePaymentForm
from pyflowcl import FlowAPI
from pyflowcl.utils import genera_parametros


class FlowProvider(BasicProvider):
    """
    FlowProvider es una clase que proporciona integración con Flow para procesar pagos.
    Inicializa una instancia de FlowProvider con el key y el secreto de Flow.

    Args:
        api_key (str): ID de receptor de Khipu.
        api_secret (str): Secreto de Khipu.
        api_medio (int | None): Versión de la API de notificaciones a utilizar (Valor por defecto: 9).
        api_endpoint (str): Ambiente flow, puede ser "live" o "sandbox" (Valor por defecto: live).
        **kwargs: Argumentos adicionales.
    """

    form_class = BasePaymentForm
    api_endpoint: str
    api_key: str = None
    api_secret: str = None
    api_medio: int = 9
    _client: Any = None

    def __init__(self, api_endpoint: str, api_key: str, api_secret: str, api_medio: int, **kwargs: int):
        super().__init__(**kwargs)
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_medio = api_medio
        self._client = FlowAPI(
            api_key=self.api_key, api_secret=self.api_secret, endpoint=self.api_endpoint, medio=self.api_medio
        )

    def get_form(self, payment, data: Optional[dict] = None) -> Any:
        """
        Genera el formulario de pago para redirigir a la página de pago de Khipu.

        Args:
            payment ("Payment"): Objeto de pago Django Payments.
            data (dict | None): Datos del formulario (opcional).

        Returns:
            Any: Formulario de pago redirigido a la página de pago de Khipu.

        Raises:
            RedirectNeeded: Redirige a la página de pago de Khipu.

        """
        if not payment.transaction_id:
            datos_para_flow = {
                "apiKey": self.api_key,
                "commerceOrder": payment.token,
                "urlReturn": payment.get_success_url(),
                "urlConfirmation": f"{get_base_url()}{payment.get_process_url()}",
                "subject": payment.description,
                "amount": int(payment.total),
                "paymentMethod": self.api_medio,
                "currency": payment.currency,
            }

            if payment.billing_email:
                datos_para_flow.update({"email": payment.billing_email})

            datos_para_flow.update(**self._extra_data(payment.attrs))

            datos_para_flow = genera_parametros(datos_para_flow, self.api_secret)
            try:
                payment.attrs.datos_flow = datos_para_flow
                payment.save()
            except Exception as e:
                raise PaymentError(f"Ocurrió un error al guardar attrs.datos_flow: {e}")

            try:
                pago = self._client.objetos.call_payment_create(parameters=datos_para_flow)

            except Exception as pe:
                payment.change_status(PaymentStatus.ERROR, str(pe))
                raise PaymentError(pe)
            else:
                payment.transaction_id = pago.token
                payment.attrs.respuesta_flow = {"url": pago.url, "token": pago.token, "flowOrder": pago.flowOrder}
                payment.save()

            raise RedirectNeeded(f"{pago.url}?token={pago.token}")

    def process_data(self, payment, request) -> JsonResponse:
        """
        Procesa los datos del pago recibidos desde Khipu.

        Args:
            payment ("Payment"): Objeto de pago Django Payments.
            request ("HttpRequest"): Objeto de solicitud HTTP de Django.

        Returns:
            JsonResponse: Respuesta JSON que indica el procesamiento de los datos del pago.

        """
        return JsonResponse("process_data")

    def _extra_data(self, attrs) -> dict:
        if "datos_extra" not in attrs:
            return {}

        data = attrs.datos_extra
        if "commerceOrder" in data:
            del data["commerceOrder"]

        if "urlReturn" in data:
            del data["urlReturn"]

        if "urlConfirmation" in data:
            del data["urlConfirmation"]

        if "amount" in data:
            del data["amount"]

        if "subject" in data:
            del data["subject"]

        if "paymentMethod" in data:
            del data["paymentMethod"]

        if "currency" in data:
            del data["currency"]

        return data

    def refund(self, payment, amount: Optional[int] = None) -> int:
        """
        Realiza un reembolso del pago.

        Args:
            payment ("Payment"): Objeto de pago Django Payments.
            amount (int | None): Monto a reembolsar (opcional).

        Returns:
            int: Monto reembolsado.

        Raises:
            PaymentError: Error al realizar el reembolso.

        """
        if payment.status != PaymentStatus.CONFIRMED:
            raise PaymentError("El pago debe estar confirmado para reversarse.")

        to_refund = amount or payment.total
        try:
            refund = self._client.payments.post_refunds(payment.transaction_id, to_refund)
        except Exception as pe:
            raise PaymentError(pe)
        else:
            payment.attrs.refund = refund
            payment.save()
            payment.change_status(PaymentStatus.REFUNDED)
            return to_refund

    def capture(self):
        """
        Captura el pago (no implementado).

        Note:
            Método no soportado por Flow.
        Raises:
            NotImplementedError: Método no implementado.
        """
        raise NotImplementedError()

    def release(self):
        """
        Libera el pago (no implementado).

        Note:
            Método no soportado por Flow.

        Raises:
            NotImplementedError: Método no implementado.

        """
        raise NotImplementedError()
