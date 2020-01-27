from django.shortcuts import render
from .models import Category
def home_view(request):
    return render(request, 'category.html')

def create_view(request):
    pass
