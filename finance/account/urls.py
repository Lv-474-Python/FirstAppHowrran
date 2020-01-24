from  django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path("register/", registration_view, name='account'),
    path('login/', login_view, name='login')
]