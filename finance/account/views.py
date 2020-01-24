from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from .models import CustomUser


def home_view(request):
    return render(request, 'good.html')


def registration_view(request):
    form = RegistrationForm(request.POST)

    if form.is_valid():

        username = form.cleaned_data.get('username')
        name = form.cleaned_data.get('name')
        surname = form.cleaned_data.get('surname')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')

        if password != password2:
            form = RegistrationForm()
            print('pass not match')
            return render(request, 'registration.html', {'form': form})

        user = CustomUser.create(username=username, password=password, email=email, name=name, surname=surname)
        if user:
            return redirect('home')

        return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

