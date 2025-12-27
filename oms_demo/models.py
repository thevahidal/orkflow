from django.db import models

from core.models import Workflowable


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(Workflowable):
    order_number = models.CharField(max_length=100)
    customer = models.ForeignKey(
        Customer, related_name="orders", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Order {self.order_number}"
