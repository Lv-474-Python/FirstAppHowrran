from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category


@login_required()
def home_view(request):
    '''render category home page'''
    categories = Category.objects.filter(user_id=request.user)

    return render(request, 'category.html', {"categories": categories})


@login_required()
def create_view(request):
    '''create new user`s category in database'''
    if request.method == 'POST':

        data = {
            "user_id": request.user,
            "name": request.POST.get('name'),
            "type": request.POST.get('category_type'),
            "description": request.POST.get('category_description')
        }

        month_limit = request.POST.get('month_limit')
        if month_limit:
            data["month_limit"] = month_limit

        Category.create(**data)
        return redirect('category_home')

    return render(request, 'category_create.html')


def edit_view(request, category_id):
    if request.method == 'POST':

        data = {
        'category_id': category_id,
        'name' : request.POST.get('name'),
        'type' : request.POST.get('type'),
        'month_limit' : request.POST.get('month_limit'),
        'description' : request.POST.get('description')
        }

        for key, value in data.items():
            print(f'{key=}, {value=}')



    category = Category.objects.get(id=category_id)
    if category.user_id == request.user:
        return render(request, 'category_edit.html', {'category':category})
    return HttpResponse('not')
