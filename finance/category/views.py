from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category


@login_required(login_url='/account/login/')
def home_view(request):
    '''render category home page'''
    categories = Category.objects.filter(user_id=request.user)

    return render(request, 'category.html', {"categories": categories})


@login_required(login_url='/account/login/')
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
        return redirect('home_category')

    return render(request, 'create_category.html')


def edit_view(request, category_id):
    category = Category.objects.get(id=category_id)
    if category.user_id == request.user:
        return HttpResponse(category.name)
    return HttpResponse('not')
