from  django.urls import path
from .views import home_view, create_view, edit_view, delete_view

urlpatterns = [
    path("", home_view, name='category_home'),
    path("create/", create_view, name='category_create'),
    path("<int:category_id>/edit", edit_view, name='category_edit'),
    path("<int:category_id>/delete", delete_view, name='category_delete'),
]
