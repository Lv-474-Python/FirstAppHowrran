from  django.urls import path
from .views import home_view, registration_view, login_view, logout_view, change_password_view

urlpatterns = [
    path('', home_view, name='home_account'),
    path("registration/", registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change_password/', change_password_view, name='change_password'),
]
