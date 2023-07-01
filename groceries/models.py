from django.db import models

from accounts.models import Seller


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Diet(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NutritionFactsLabel(models.Model):
    fats = models.DecimalField(max_digits=6, decimal_places=2)
    saturated_fats = models.DecimalField(max_digits=6, decimal_places=2)
    polyunsaturated_fats = models.DecimalField(max_digits=6, decimal_places=2)
    monounsaturated_fats = models.DecimalField(max_digits=6, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=2)
    dietary_fiber = models.DecimalField(max_digits=6, decimal_places=2)
    sugars = models.DecimalField(max_digits=6, decimal_places=2)
    proteins = models.DecimalField(max_digits=6, decimal_places=2)
    calories = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Nutrition facts (per 100 grams) for {self.grocery}'


class Grocery(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    diets = models.ManyToManyField(Diet)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    nutrition_facts_label = models.OneToOneField(NutritionFactsLabel, on_delete=models.CASCADE)
    creator = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'groceries'

    def __str__(self):
        return self.name
