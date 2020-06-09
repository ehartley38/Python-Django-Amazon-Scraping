from django.shortcuts import render
from django.http import HttpResponse
from .models import Item


details = [
    {
        'username': 'ehart',
        'email': 'ehartley38@gmail.com',
        'date_joined': '8/6/2020'
    },
    {
        'username': 'eddy',
        'email': 'ehartley11@gmail.com',
        'date_joined': '8/6/2019'
    }
]



# Create your views here.
def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'item_searcher/home.html', context)

def about(request):
    return render(request, 'item_searcher/about.html', {'title': 'About'})

def help(request):
    return HttpResponse('<h1>Help</h1>')