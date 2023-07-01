from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from accounts.decorators import allowed_users
from accounts.models import User
from groceries.forms import NutritionFactsLabelForm, GroceryForm
from groceries.models import Category, Diet, Grocery
from orders.models import Order, OrderItem


# Create your views here.


def home(request):
    return render(request, 'groceries/home.html')


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER, User.Role.SELLER, User.Role.ADMINISTRATOR,))
def groceries(request):
    all_groceries = Grocery.objects.all().order_by('name')

    category = request.GET.get('category')
    if category is not None:
        all_groceries = all_groceries.filter(categories__name__in=[category]).all().order_by('name')
    diet = request.GET.get('diet')
    if diet is not None:
        all_groceries = all_groceries.filter(diets__name__in=[diet]).all().order_by('name')

    page = Paginator(all_groceries, 9)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {'categories': Category.objects.all(), 'diets': Diet.objects.all(), 'page': page}
    return render(request, 'groceries/groceries.html', context)


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER, User.Role.SELLER, User.Role.ADMINISTRATOR,))
def grocery_details(request, grocery_id):
    grocery = Grocery.objects.filter(id=grocery_id).first()

    context = {'grocery': grocery}
    return render(request, 'groceries/grocery-details.html', context)


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.SELLER,))
def add_grocery(request):
    nutrition_facts_label_form_errors = None
    grocery_form_errors = None
    if request.method == 'POST':
        nutrition_facts_label_form = NutritionFactsLabelForm(request.POST, request.FILES)
        grocery_form = GroceryForm(request.POST, request.FILES)
        if all((nutrition_facts_label_form.is_valid(), grocery_form.is_valid())):
            nutrition_facts_label = nutrition_facts_label_form.save()
            grocery = grocery_form.save(commit=False)
            grocery.creator = request.user
            grocery.nutrition_facts_label = nutrition_facts_label
            grocery.save()
            grocery.categories.set(grocery_form.cleaned_data['categories'])
            grocery.diets.set(grocery_form.cleaned_data['diets'])
            grocery.save()

            return redirect('groceries:groceries')
        else:
            nutrition_facts_label_form_errors = nutrition_facts_label_form.errors
            grocery_form_errors = grocery_form.errors

    context = {'categories': Category.objects.all(), 'diets': Diet.objects.all(),
               'nutrition_facts_label_form_errors': nutrition_facts_label_form_errors,
               'grocery_form_errors': grocery_form_errors}
    return render(request, 'groceries/add-grocery.html', context)


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.SELLER,))
def edit_grocery(request, grocery_id):
    grocery = Grocery.objects.get(id=grocery_id)
    nutrition_facts_label_form_errors = None
    grocery_form_errors = None
    if request.method == 'POST':
        nutrition_facts_label_form = NutritionFactsLabelForm(request.POST, request.FILES)
        grocery_form = GroceryForm(request.POST, request.FILES)
        if all((nutrition_facts_label_form.is_valid(), grocery_form.is_valid())):
            grocery.nutrition_facts_label.fats = nutrition_facts_label_form.cleaned_data['fats']
            grocery.nutrition_facts_label.saturated_fats = nutrition_facts_label_form.cleaned_data['saturated_fats']
            grocery.nutrition_facts_label.polyunsaturated_fats = nutrition_facts_label_form.cleaned_data[
                'polyunsaturated_fats']
            grocery.nutrition_facts_label.monounsaturated_fats = nutrition_facts_label_form.cleaned_data[
                'monounsaturated_fats']
            grocery.nutrition_facts_label.carbohydrates = nutrition_facts_label_form.cleaned_data['carbohydrates']
            grocery.nutrition_facts_label.dietary_fiber = nutrition_facts_label_form.cleaned_data['dietary_fiber']
            grocery.nutrition_facts_label.sugars = nutrition_facts_label_form.cleaned_data['sugars']
            grocery.nutrition_facts_label.proteins = nutrition_facts_label_form.cleaned_data['proteins']
            grocery.nutrition_facts_label.calories = nutrition_facts_label_form.cleaned_data['calories']
            grocery.nutrition_facts_label.save()

            grocery.name = grocery_form.cleaned_data['name']
            grocery.description = grocery_form.cleaned_data['description']
            grocery.categories.set(grocery_form.cleaned_data['categories'])
            grocery.diets.set(grocery_form.cleaned_data['diets'])
            grocery.price = grocery_form.cleaned_data['price']
            grocery.quantity = grocery_form.cleaned_data['quantity']
            grocery.image = grocery_form.cleaned_data['image']
            grocery.save()

            return redirect('groceries:grocery_details', grocery_id)
        else:
            nutrition_facts_label_form_errors = nutrition_facts_label_form.errors
            grocery_form_errors = grocery_form.errors

    context = {'categories': Category.objects.all(), 'diets': Diet.objects.all(),
               'nutrition_facts_label_form_errors': nutrition_facts_label_form_errors,
               'grocery_form_errors': grocery_form_errors, 'grocery': grocery}
    return render(request, 'groceries/edit-grocery.html', context)


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.SELLER,))
def delete_grocery(request, grocery_id):
    if request.method == 'POST':
        grocery = Grocery.objects.get(id=grocery_id)
        grocery.nutrition_facts_label.delete()
        grocery.delete()

    return redirect('groceries:groceries')


@login_required(login_url='accounts:login')
@allowed_users(roles=(User.Role.CONSUMER,))
def add_to_cart(request, grocery_id):
    grocery = Grocery.objects.filter(id=grocery_id).first()
    consumer = request.user
    order, created = Order.objects.get_or_create(consumer=consumer, complete=False)
    if order is None:
        order = created
    order_item = order.orderitem_set.filter(grocery=grocery).first()
    if order_item:
        order_item.quantity += 1
    else:
        order_item = OrderItem()
        order_item.grocery = grocery
        order_item.order = order
    order_item.save()

    return redirect('orders:shopping_cart')
