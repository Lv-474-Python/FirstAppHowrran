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
    months1 = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
               7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    # make list of months from the past year to current
    # E.G. if today is February:
    # months = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
    #           'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']

    months = [months1[(i % 13)] for i in range(current_month + 1,
                                               current_month + 14) if i != 13]

    # income_per_month is a dict that save income for each month
    # months are in their number equivalent
    # months{1:100} means that in Jan user had 100 income
    income_per_month1 = Operation.get_category_income_per_month(request.user,
                                                                category_id)
    income_per_month = {}
    for i in range(current_month + 1, current_month + 14):
        if i == 13: continue
        i %= 13
        income_per_month[i] = income_per_month1[i]

    # outcome_per_month is a dict that save outcome for each month
    # months are in their number equivalent
    # months{1:50} means that in Jan user had 50 outcome
    outcome_per_month1 = Operation.get_category_outcome_per_month(request.user,
                                                                  category_id)
    outcome_per_month = {}
    for i in range(current_month + 1, current_month + 14):
        if i == 13: continue
        i %= 13
        outcome_per_month[i] = outcome_per_month1[i]

    if category.type == 'Current':
        income_per_month, outcome_per_month = outcome_per_month, income_per_month

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

    fig.update_layout(barmode='group', width=1425, height=600)

    # html <div> with Bar Chart
    bar = plot(fig, output_type='div')

    return render(request,
                  'statistic_category.html',
                  {'category': category,
                   'operation_list': operation_list,
                   'category_income': category_income,
                   'category_outcome': category_outcome,
                   'bar': bar})
