from payments.models import BasePayment

class FlowTestPayment(BasePayment):
    """Payment model subclassing the BasePayment model"""

    def get_failure_url(self):
        return "https://example.com/failure"

    def get_success_url(self):
        return "https://example.com/success"
