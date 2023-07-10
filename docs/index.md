# django-payments-flow

`Proyecto en desarrollo activo, no listo para produccion`

`django-payments-flow` es una variante de Django Payments que implementa la
creación, confirmación y expiración de pagos realizados a través de Flow. Este
módulo proporciona integración con la API de Flow para facilitar el
procesamiento y gestión de pagos en tu aplicación web Django.


## Introducción

`django-payments-flow` está diseñado para simplificar la integración de
pagos de Flow en tu proyecto Django Payments. Con este módulo, puedes crear y
gestionar pagos utilizando la pasarela de pago de Flow de manera sencilla.

Características principales:

- Crea y procesa pagos de forma segura con Flow.
- Recibe notificaciones de confirmación de pago.
- Maneja automáticamente la expiración y cancelación de pagos.

## Instalación

Puedes instalar django-payments-flow con:

=== "usando pip"
    ```shell
    pip install django-payments-flow
    ```
=== "usando poetry"
    ```shell
    poetry add django-payments-flow
    ```

## Configuración

La configuracion se realiza como una variante de Django Payments

```python
PAYMENT_VARIANTS = {
    "flow": ("django_payments_flow.KhipuProvider", {
        "key": 1,
        "secret": "qwertyasdf0123456789",
    })
}
```
