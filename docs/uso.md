# Como Usar

## Instalación

Para utilizar el módulo `django-payments-flow`, puedes realizar la instalación mediante el uso de pip o poetry.

=== "usando pip"
    ```shell
    pip install django-payments-flow
    ```
=== "usando poetry"
    ```shell
    poetry add django-payments-flow
    ```

## Configuración

La configuración del módulo django-payments-flow se realiza como una variante
de Django Payments. Debes agregar la siguiente configuración en tu archivo de
configuración de Django:

```python
PAYMENT_VARIANTS = {
    "flow": ("django_payments_flow.KhipuProvider", {
        "receiver_id": 1,
        "secret": "qwertyasdf0123456789",
    })
}
```

### Variables de configuración

* `receiver_id`: Este valor corresponde a la cuenta entregada por Khipu para
identificar al receptor de los pagos.
* `secret`: Este valor corresponde a la contraseña entregada por Khipu para
autenticar la comunicación con su plataforma.

## Datos Extra

El módulo `django-payments-flow` permite enviar datos extra en cada pago. Para
hacerlo, debes utilizar un objeto JSON dentro de la propiedad "attrs" del
modelo de Pagos.

Por ejemplo, si deseas enviar el nombre del cliente en cada compra, puedes
utilizar el siguiente código:
```python
datos_extra: dict = {
    "payer_name": "Nombre de Cliente",
}
payment.attrs.datos_extra = datos_extra
payment.save()
```

Puedes proporcionar un diccionario unidimensional con los valores extra que
deseas enviar en cada pago.

Cabe destacar que los valores `payer_email`no pueden ser utilizados
como datos extra y serán ignorados al momento de crear el pago.
