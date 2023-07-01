from django.contrib import admin

from groceries.models import Category, Diet, NutritionFactsLabel, Grocery


# Register your models here.

class GroceriesInCategoryInline(admin.StackedInline):
    model = Grocery.categories.through
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [GroceriesInCategoryInline, ]


class GroceriesInDietInline(admin.StackedInline):
    model = Grocery.diets.through
    extra = 0


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    inlines = [GroceriesInDietInline, ]


admin.site.register(NutritionFactsLabel)


@admin.register(Grocery)
class GroceryAdmin(admin.ModelAdmin):
    readonly_fields = ['date_created', 'date_modified']
