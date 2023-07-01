from django.contrib import admin

from orders.models import Order, OrderItem, ShippingInformation, PaymentDetails, Checkout


# Register your models here.

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ]
    readonly_fields = ['date_ordered']
    list_filter = ['complete']


admin.site.register(OrderItem)
admin.site.register(ShippingInformation)
admin.site.register(PaymentDetails)
admin.site.register(Checkout)
