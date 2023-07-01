from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.shopping_cart, name='shopping_cart'),
    path('<int:order_item_id>/increase-quantity', views.increase_quantity, name='increase-order-item-quantity'),
    path('<int:order_item_id>/decrease-quantity', views.decrease_quantity, name='decrease-order-item-quantity'),
    path('<int:order_item_id>/remove', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('order-items-count/', views.order_items_count, name='order_items_counts'),
]
