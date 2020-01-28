from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, \
    update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .models import CustomUser


@login_required
def home_view(request):
    '''render home html'''
    return render(request, 'good.html')


def registration_view(request):
    '''take arguments from registration form and create new user'''
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

    return render(request, 'reg2.html')


def login_view(request):
    '''render login page and authenticate the user'''
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get("username")
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user and user.is_active:
        login(request, user)
        return redirect('home_account')

    return redirect('login')


@login_required
def logout_view(request):
    '''logout the user'''
    logout(request)
    return redirect('login')


def change_password_view(request):
    '''change users password'''
    if request.method == 'POST':
        current_password = request.user.password
        username = request.user.username
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if check_password(old_password, current_password):
            user = CustomUser.change_password(username=username,
                                              new_password=new_password)
            update_session_auth_hash(request, user)

            return redirect('home_account')

    return render(request, 'change_password.html')
