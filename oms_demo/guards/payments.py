from django.core.exceptions import ValidationError
from core.guards.base import StateGuard


class PaymentCompletedGuard(StateGuard):
    def can_exit(self, instance):
        if not instance.payment_completed:
            raise ValidationError("Payment is not completed")

    def can_enter(self, instance):
        pass
