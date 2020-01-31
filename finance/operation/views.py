from django.shortcuts import render, redirect
from category.models import Category
from .models import Operation


def home_view(request):
    return render(request, 'operation.html')


def create_view(request):
    if request.method == 'POST':
        to_category = request.POST.get('to')
        from_category = request.POST.get('from')
        value = request.POST.get('value')
        date = request.POST.get('date')

        print(f'{to_category=} {from_category=} {value=} {date=}')

        from_category_obj = Category.get_category_by_name(user_id=request.user, name=from_category)
        to_category_obj = Category.get_category_by_name(user_id=request.user, name=to_category)

        Operation.create(from_category_obj, to_category_obj, value, date)
        return redirect('operation_home')

    user_category = Category.get_user_category(user_id=request.user)

    return render(request, 'operation_create.html',
                  {'user_category': user_category})
