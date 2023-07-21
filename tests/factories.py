import factory
from factory.django import DjangoModelFactory
from payments import PaymentStatus, get_payment_model

from tests.test_app.models import BasePayment


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = get_payment_model()

    total = factory.Faker("pydecimal", min_value=5000, max_value=6000, right_digits=0)
    currency = "CLP"
    description = factory.Faker("sentence")

    class Params:
        submitted = factory.Trait(
            status=PaymentStatus.INPUT,
            transaction_id="tr_12345",
        )
