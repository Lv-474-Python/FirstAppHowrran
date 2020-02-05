from django.shortcuts import render
from operation.models import Operation
from category.models import Category
from plotly.offline import plot

import datetime
import plotly.express as px
import plotly.graph_objects as go


def home_view(request):
    categories, income = Operation.get_user_income_by_category(request.user)
    categories2, outcome2 = Operation.get_user_outcome_by_category(
                                                               request.user)

    fig_income = px.pie(categories,
                        categories,
                        income,
                        title={
                            'text': "Income",
                            'y': 0.9,
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {'family': 'Arial',
                                     'size': 20
                                     }
                        },

                        width=500,
                        height=450)

    fig_outcome = px.pie(categories2,
                         categories2,
                         outcome2,
                         title={
                             'text': "Outcome",
                             'y': 0.9,
                             'x': 0.45,
                             'xanchor': 'center',
                             'yanchor': 'top',
                             'font': {'family': 'Arial',
                                      'size': 20
                                      }
                         },
                         width=500,
                         height=450)

    # plot(fig, filename='statistic/templates/piechart_income')
    pie_income = plot(fig_income, output_type='div')
    pie_outcome = plot(fig_outcome, output_type='div')

    income = Operation.get_user_income(request.user)
    outcome = Operation.get_user_outcome(request.user)
    current = Operation.get_user_current(request.user)
    operation_list = Operation.get_user_operation(request.user)
    user_category = Category.get_user_category(request.user)

    request.session['current'] = current

    return render(request,
                  'statistic.html',
                  {'income': income,
                   'outcome': outcome,
                   'current': current,
                   'operation_list': operation_list,
                   'user_category': user_category,
                   'pie_income': pie_income,
                   'pie_outcome': pie_outcome})


def statistic_category_view(request, category_id):
    '''

    :param request:
    :param category_id:
    :return: list of category operations, category total income/outcome
     and bar plot of income\outcome of the category for the last year

    '''
    category = Category.get_category(category_id)
    operation_list = Operation.get_user_operation_by_category(request.user,
                                                              category_id)
    category_income = Operation.get_user_category_income(request.user,
                                                         category_id)

    category_outcome = Operation.get_user_category_outcome(request.user,
                                                           category_id)

    current_month = datetime.datetime.today().month
    months1 = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
              7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    months = [months1[(i % 12)] for i in range(current_month + 1, current_month + 13) if i != 12]


    income_per_month1 = Operation.get_category_income_per_month(request.user,
                                                               category_id)
    income_per_month = {}
    for i in range(current_month + 1, current_month + 13):
        if i == 12: continue
        i %= 12
        income_per_month[i] = income_per_month1[i]

    outcome_per_month1 = Operation.get_category_outcome_per_month(request.user,
                                                                category_id)
    outcome_per_month = {}
    for i in range(current_month + 1, current_month + 13):
        if i == 12: continue
        i %= 12
        outcome_per_month[i] = outcome_per_month1[i]


    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=months,
        y=list(income_per_month.values()),
        name='Income',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=list(outcome_per_month.values()),
        name='Outcome',
        marker_color='blue'
    ))


    fig.update_layout(barmode='group')

    bar = plot(fig, output_type='div')

    return render(request,
                  'statistic_category.html',
                  {'category': category,
                   'operation_list': operation_list,
                   'category_income': category_income,
                   'category_outcome': category_outcome,
                   'bar': bar})
