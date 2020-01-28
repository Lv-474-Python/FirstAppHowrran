from django.shortcuts import render, redirect
from .models import Category


def home_view(request):
    '''render category home page'''
    categories = Category.objects.all()
    user_categories = Category.objects.filter(user_id=request.user)
    print(user_categories)

    return render(request, 'category.html', {"categories": categories,
                                             'user_categories': user_categories})


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
