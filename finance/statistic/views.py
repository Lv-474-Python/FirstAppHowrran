from django.shortcuts import render
from operation.models import Operation
from category.models import Category


def home_view(request):
    income = Operation.get_user_income(request.user)
    outcome = Operation.get_user_outcome(request.user)
    current = Operation.get_user_current(request.user)
    operation_list = Operation.get_user_operation(request.user)
    user_category = Category.get_user_category(request.user)

    return render(request, 'statistic.html',
                  {'income': income, 'outcome': outcome, 'current': current,
                   'operation_list': operation_list,
                   'user_category': user_category})


def statistic_category_view(request, category_id):

    category = Category.get_category(category_id)
    category_name = category.name
    operation_list = Operation.get_user_operation_by_category(request.user,
                                                              category_id)
    category_income = Operation.get_user_category_income(request.user,
                                                         category_id)

    category_outcome = Operation.get_user_category_outcome(request.user,
                                                           category_id)

    return render(request, 'statistic_category.html',
                  {'category_name':category_name,
                   'operation_list': operation_list,
                   'category_income':category_income,
                   'category_outcome':category_outcome})
