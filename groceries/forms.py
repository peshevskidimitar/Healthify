from django import forms

from groceries.models import Grocery, NutritionFactsLabel


class GroceryForm(forms.ModelForm):
    class Meta:
        model = Grocery
        exclude = ('creator', 'nutrition_facts_label')


class NutritionFactsLabelForm(forms.ModelForm):
    class Meta:
        model = NutritionFactsLabel
        fields = '__all__'
