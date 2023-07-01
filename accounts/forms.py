from django.contrib.auth.forms import UserCreationForm

from accounts.models import Consumer


class CustomConsumerCreationForm(UserCreationForm):
    class Meta:
        model = Consumer
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
