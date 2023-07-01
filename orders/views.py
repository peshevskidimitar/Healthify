from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.decorators import allowed_users
from accounts.models import User
from orders.forms import ShippingInformationForm, PaymentDetailsForm
from orders.models import Order, Checkout


# Create your views here.


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER,))
def shopping_cart(request):
    consumer = request.user
    order, created = Order.objects.get_or_create(consumer=consumer, complete=False)
    if order is None:
        order = created
    items = order.orderitem_set.all()

    context = {'items': items, 'total_price': order.total}
    return render(request, 'orders/shopping-cart.html', context)


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER,))
def increase_quantity(request, order_item_id):
    consumer = request.user
    order, created = Order.objects.get_or_create(consumer=consumer, complete=False)
    if order is None:
        order = created
    order_item = order.orderitem_set.filter(id=order_item_id).first()
    if order_item:
        order_item.quantity += 1
        order_item.save()

    return redirect('orders:shopping_cart')


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER,))
def decrease_quantity(request, order_item_id):
    consumer = request.user
    order, created = Order.objects.get_or_create(consumer=consumer, complete=False)
    if order is None:
        order = created
    order_item = order.orderitem_set.filter(id=order_item_id).first()
    if order_item and order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()

    return redirect('orders:shopping_cart')


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER,))
def remove_from_cart(request, order_item_id):
    if request.method == 'POST':
        consumer = request.user
        order, created = Order.objects.get_or_create(consumer=consumer, complete=False)
        if order is None:
            order = created
        order_item = order.orderitem_set.filter(id=order_item_id).first()
        if order_item:
            order_item.delete()

    return redirect('orders:shopping_cart')


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER,))
def checkout(request):
    shipping_information_form_errors = None
    payment_details_form_errors = None
    if request.method == 'POST':
        shipping_information_form = ShippingInformationForm(request.POST)
        payment_details_form = PaymentDetailsForm(request.POST)
        if all((shipping_information_form.is_valid(), payment_details_form.is_valid())):
            consumer = request.user
            order, created = Order.objects.get_or_create(consumer=consumer, complete=False)
            if order is None:
                order = created
            order.complete = True
            order.save()
            checkout_obj = Checkout()
            checkout_obj.consumer = consumer
            checkout_obj.order = order
            checkout_obj.shipping_information = shipping_information_form.save()
            checkout_obj.payment_details = payment_details_form.save()
            checkout_obj.save()

            return redirect('orders:confirmation')
        else:
            shipping_information_form_errors = shipping_information_form.errors
            payment_details_form_errors = payment_details_form.errors

    context = {'shipping_information_form_errors': shipping_information_form_errors,
               'payment_details_form_errors': payment_details_form_errors}
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER,))
def confirmation(request):
    return render(request, 'orders/confirmation.html')


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER,))
def order_items_count(request):
    consumer = request.user
    order, created = Order.objects.get_or_create(consumer=consumer, complete=False)
    if order is None:
        order = created

    return JsonResponse({'count': len(order.orderitem_set.all())})
