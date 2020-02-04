from django.shortcuts import render
from operation.models import Operation
from category.models import Category
from plotly.offline import plot
import plotly.express as px


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
    category = Category.get_category(category_id)
    operation_list = Operation.get_user_operation_by_category(request.user,
                                                              category_id)
    category_income = Operation.get_user_category_income(request.user,
                                                         category_id)

    category_outcome = Operation.get_user_category_outcome(request.user,
                                                           category_id)

    return render(request, 'statistic_category.html',
                  {'category': category,
                   'operation_list': operation_list,
                   'category_income': category_income,
                   'category_outcome': category_outcome})
