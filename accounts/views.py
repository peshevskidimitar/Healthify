from django.contrib import auth, messages
from django.shortcuts import render, redirect

from accounts.decorators import unauthenticated
from accounts.forms import CustomConsumerCreationForm


# Create your views here.


@unauthenticated(redirect_url='/')
def register(request):
    errors = None
    if request.method == 'POST':
        form = CustomConsumerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    context = {'errors': errors}
    return render(request, 'accounts/register.html', context)


@unauthenticated(redirect_url='/')
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)

            redirect_url = request.GET.get('next')
            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect('/')
        else:
            messages.error(request, 'Username or password is incorrect.')

    context = {}
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth.logout(request)

    return redirect('accounts:login')


def unauthorized(request):
    return render(request, 'accounts/unauthorized.html')
