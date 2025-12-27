from django.utils.translation import gettext_lazy as _
from django.db import models

from core.models import Workflowable


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(Workflowable):
    class PaymentStatus(models.TextChoices):
        waiting_for_payment = "waiting_for_payment", _("waiting_for_payment")
        paid = "paid", _("paid")

    order_number = models.CharField(max_length=100)
    customer = models.ForeignKey(
        Customer, related_name="orders", on_delete=models.CASCADE
    )
    payment_status = models.CharField(
        choices=PaymentStatus.choices, default=PaymentStatus.waiting_for_payment
    )

    def __str__(self):
        return f"Order {self.order_number}"

    @property
    def payment_completed(self):
        return self.payment_status == Order.PaymentStatus.paid
