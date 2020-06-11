from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from .forms import ItemSearchForm




def home(request):
    #Home page item search bar
    if request.method == 'POST':
        form = ItemSearchForm(request.POST)
        if form.is_valid():
            form.save()
            product = form.cleaned_data.get('name')
    else:
        form = ItemSearchForm()

    context = {
        'items': Item.objects.all(),
        'form': form
    }
    return render(request, 'item_searcher/home.html', context)

def about(request):
    return render(request, 'item_searcher/about.html', {'title': 'About'})

def help(request):
    return HttpResponse('<h1>Help</h1>')