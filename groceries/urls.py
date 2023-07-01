from django.urls import path
from . import views

app_name = 'groceries'

urlpatterns = [
    path('', views.home, name='home'),
    path('groceries/', views.groceries, name='groceries'),
    path('groceries/<int:grocery_id>', views.grocery_details, name='grocery_details'),
    path('groceries/add', views.add_grocery, name='add_grocery'),
    path('groceries/<int:grocery_id>/edit', views.edit_grocery, name='edit_grocery'),
    path('groceries/<int:grocery_id>/delete', views.delete_grocery, name='delete_grocery'),
    path('<int:grocery_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
]
