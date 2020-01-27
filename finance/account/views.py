from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .models import CustomUser


@login_required
def home_view(request):
    return render(request, 'good.html')


# def registration_view(request):
#     form = RegistrationForm(request.POST)
#
#     if form.is_valid():
#
#         username = form.cleaned_data.get('username')
#         name = form.cleaned_data.get('name')
#         surname = form.cleaned_data.get('surname')
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password')
#         password2 = form.cleaned_data.get('password2')
#
#         if password != password2:
#             form = RegistrationForm()
#             print('pass not match')
#             return render(request, 'reg2.html', {'form': form})
#
#         user = CustomUser.create(username=username, password=password,
#                                  email=email, name=name, surname=surname)
#         if user:
#             return redirect('home')
#
#         return redirect('home')
#     else:
#         form = RegistrationForm()
#
#     return render(request, 'reg2.html', {'form': form})
#
def registration_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            print('pass not match')
            return render(request, 'reg2.html')

        user = CustomUser.create(username=username, password=password,
                                 email=email, name=name, surname=surname)
        if user:
            return redirect('login')

        return redirect('login')

    else:
        return render(request, 'reg2.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get("username")
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user and user.is_active:
        login(request, user)
        return redirect('home')

    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')

def change_password_view(request):
    # TODO write change pasword function and template
    if request.method =='POST':
        pass

    return render(request, 'change_password.html')

