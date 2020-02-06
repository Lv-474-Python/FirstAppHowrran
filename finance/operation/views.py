from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from category.models import Category
from .models import Operation
from django.http import HttpResponse
from plotly.offline import plot

import plotly.graph_objects as go
import datetime

@login_required
def home_view(request):
    user_operation = Operation.get_user_operation(request.user.id)
    if user_operation:
        if request.user != user_operation[0].to_category.user_id:
            return HttpResponse("403 NOT ALLOWED")
    # get income of all user categories in dict
    # {month:income}
    inc = Operation.get_income_of_all_categories_per_month(request.user)
    out = Operation.get_outcome_of_all_categories_per_month(request.user)

    current_month = datetime.datetime.today().month
    months1 = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
               7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    income = {}
    outcome = {}

    # make list of months from the past year to current
    # E.G. if today is February:
    # months = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
    #           'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
    months = [months1[(i % 13)] for i in range(current_month + 1,
                                               current_month + 14) if i != 13]

    for i in range(current_month + 1, current_month + 14):
        if i == 13: continue
        i %= 13
        income[i] = inc[i]
        outcome[i] = out[i]




    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=months,
        y=list(income.values()),
        name='Income',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=list(outcome.values()),
        name='Outcome',
        marker_color='blue'
    ))

    fig.update_layout(barmode='group',
                      title={
                          'text': "Total Income\Outcome",
                          'y': 0.9,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top',
                          'font': {'family': 'Arial',
                                   'size': 20
                                   }
                      },
                      width=1425,
                      height=600)

    # html <div> with Bar Chart
    bar = plot(fig, output_type='div')

    return render(request, 'operation.html',
                  {'user_operation': user_operation,
                   'bar': bar})


@login_required
def create_view(request):
    user_category = Category.get_user_category(user_id=request.user)

    if request.method == 'POST':
        to_category = request.POST.get('to')
        from_category = request.POST.get('from')
        value = request.POST.get('value')
        date = request.POST.get('date')

        from_category_obj = Category.get_category_by_name(user_id=request.user,
                                                          name=from_category)
        to_category_obj = Category.get_category_by_name(user_id=request.user,
                                                        name=to_category)

        if from_category_obj.type == to_category_obj.type or (
                from_category_obj.type != "Current"
                and to_category_obj.type != 'Current'):
            return HttpResponse('ONE CATEGORY MUST BE CURRENT')
        Operation.create(from_category_obj, to_category_obj, value, date)
        return redirect('operation_home')

    return render(request, 'operation_create.html',
                  {'user_category': user_category})
