from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegistrationForm
#from .models import MyUser

# Create your views here.

def home_view(request):
    return render(request, 'good.html')


def registration_view(request):
    form = RegistrationForm(request.POST)

    if form.is_valid():

        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        print(password1, password2)
        if password1 != password2:
            form = RegistrationForm()
            print('pass not match')
            return render(request, 'registration.html', {'form': form})

        user = form.save()
        user.set_password(user.password)
        user.save()
        # user = authenticate(email=email, password=password)
        print('redirecting........')
        return redirect('home')
    else:
        form = RegistrationForm()
        print('wrong')
    return render(request, 'registration.html', {'form': form})
