from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Item
from .forms import ItemSearchForm
from django.views.generic import ListView, DetailView, CreateView




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

class ItemListView(ListView):
    model = Item
    template_name = 'item_searcher/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'items'
    ordering = ['price'] #Orders items by price

class ItemDetailView(DetailView): #View for more detail on item when you click on it
    model = Item

class ItemCreateView(LoginRequiredMixin, CreateView): #View with a form where we create a new post
    model = Item
    fields = ['name', 'description', 'price']

    #Override the form_valid method
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



def about(request):
    return render(request, 'item_searcher/about.html', {'title': 'About'})

def help(request):
    return HttpResponse('<h1>Help</h1>')