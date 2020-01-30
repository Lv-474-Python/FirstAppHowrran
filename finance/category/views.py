from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from .models import Category


@login_required()
def home_view(request):
    '''render category home page'''
    categories = reversed(Category.objects.filter(user_id=request.user))
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
    category = Category.get_category(id=category_id)
    if category:
        if request.method == 'POST':

            data = {
                'category_id': category_id,
                'name': request.POST.get('name'),
                'type': request.POST.get('category_type'),
                'month_limit': request.POST.get('month_limit'),
                'description': request.POST.get('description')
            }

            change_data = dict()

            for key, value in data.items():
                if value and value != category_id:
                    change_data[key] = value

            Category.update(category_id, change_data)
            return redirect('category_home')

        if category.user_id == request.user:
            return render(request, 'category_edit.html',
                          {'category': category})
        return HttpResponse('not allowed')
    return HttpResponse('not found')


def delete_view(request, category_id):
    category = Category.get_category(id=category_id)
    if category:
        if category.user_id == request.user:
            category.delete_category(category_id)
            return redirect('category_home')
        return HttpResponse('not allowed')
    return HttpResponse('not found')
