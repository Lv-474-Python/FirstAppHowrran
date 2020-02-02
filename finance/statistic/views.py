from django.shortcuts import render
from operation.models import Operation


def home_view(request):
    income = Operation.get_user_income(request.user)
    outcome = Operation.get_user_outcome(request.user)
    current = Operation.get_user_current(request.user)
    return render(request, 'statistic.html',
                  {'income': income, 'outcome': outcome, 'current': current})
