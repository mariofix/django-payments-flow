import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def flow_payment():
    from pyflowcl.Clients import ApiClient
    from pyflowcl import Payment

    transaction_id = fake.uuid4()
    currency = fake.currency_code()
    amount = fake.pydecimal(right_digits=0, min_value=5000, max_value=6000)
    description = fake.sentence()
    checkout_url = (
        f"https://sandbox.flow.cl/app/web/pay.php?token={fake.password(length=10,special_chars=False)}",
    )

    data = {
        "id": transaction_id,
        "amount": {
            "currency": currency,
            "value": str(amount),
        },
        "status": "open",
        "description": description,
        "_links": {
            "checkout": {
                "href": checkout_url,
                "type": "text/html",
            },
        },
    }
    return Payment(data, None)
