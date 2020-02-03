from django.shortcuts import render, redirect
from category.models import Category
from .models import Operation
from django.http import JsonResponse, HttpResponse


def home_view(request):

    #a = Operation.get_user_operation_by_category(request.user)
    user_operation = Operation.get_user_operation(request.user.id)
    return render(request, 'operation.html',
                  {'user_operation': user_operation})


def create_view(request):
    user_category = Category.get_user_category(user_id=request.user)

    if request.method == 'POST':
        to_category = request.POST.get('to')
        from_category = request.POST.get('from')
        value = request.POST.get('value')
        date = request.POST.get('date')

        print(f'{to_category=} {from_category=} {value=} {date=}')

        from_category_obj = Category.get_category_by_name(user_id=request.user,
                                                          name=from_category)
        to_category_obj = Category.get_category_by_name(user_id=request.user,
                                                        name=to_category)
        if from_category_obj.type == to_category_obj.type:
            return HttpResponse('DONT CHOOSE SAME TYPE')
        Operation.create(from_category_obj, to_category_obj, value, date)
        return redirect('operation_home')



    return render(request, 'operation_create.html',
                  {'user_category': user_category})
