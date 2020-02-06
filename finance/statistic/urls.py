from django.urls import path, include
from .views import home_view, statistic_category_view, detail_view

urlpatterns = [
    path('', home_view, name='statistic_home'),
    path('detail/', detail_view, name='statistic_detail'),
    path('<int:category_id>/statistic', statistic_category_view,
         name='statistic_category'),

]
