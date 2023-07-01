from django.db import models

from accounts.models import Consumer
from groceries.models import Grocery


# Create your models here.


class Order(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    @property
    def total(self):
        total_price = 0
        for order_item in self.orderitem_set.all():
            total_price += order_item.subtotal

        return total_price

    def __str__(self):
        return f'Order No. {self.id} ({self.consumer})'


class OrderItem(models.Model):
    grocery = models.ForeignKey(Grocery, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.grocery.price * self.quantity

    def __str__(self):
        return f'Grocery: {self.grocery}, Quantity: {self.quantity}'


class ShippingInformation(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.full_name} - {self.address}, {self.city}'


class PaymentDetails(models.Model):
    online_payment = models.BooleanField(default=False)
    card_holder = models.CharField(max_length=255, blank=True)
    card_number = models.CharField(max_length=255, blank=True)
    card_code = models.CharField(max_length=255, blank=True)
    expiry_date = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Payment details'


class Checkout(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_information = models.ForeignKey(ShippingInformation, on_delete=models.CASCADE)
    payment_details = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.consumer} - {self.order}'
