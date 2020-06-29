from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView, ListView

from . import site_scraper
from .forms import ItemSearchForm, ItemTrackingForm
from .models import Item, TrackingDetails

'''
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
    return render(request, 'item_searcher/home.html', context)'''


class ItemSearchView(FormView):
    template_name = 'item_searcher/home.html'  # <app>/<model>_<viewtype>.html
    form_class = ItemSearchForm

    def form_valid(self, form):
        product = site_scraper.gather_info(form.cleaned_data.get('url'))
        item = Item.objects.create(name=product.title, price=product.price)
        item.save()
        self.success_url ='trackinginfo/'+ str(item.pk) + '/'
        return super().form_valid(form)

#User enters tracking info here
class ItemTrackingView(FormView):
    template_name = 'item_searcher/item_tracking_info.html'
    form_class = ItemTrackingForm
    success_url = '/list/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['item'] = Item.objects.get(pk=self.kwargs['pk'])
        return data

    def form_valid(self, form):
        #self.success_url = 'list/'
        target_price = form.cleaned_data.get('target_price')
        item = self.get_context_data()['item']
        tracking_info = TrackingDetails.objects.create(current_price=item.price, start_price=item.price, target_price=target_price,
                                                       user=self.request.user, item=item)
        tracking_info.save()
        return super().form_valid(form)




class ItemDetailView(DetailView):  # View for more detail on item when you click on it
    model = TrackingDetails
    template_name = 'item_searcher/item_detail.html'


class ItemCreateView(LoginRequiredMixin, CreateView):  # View with a form where we create a new post
    model = Item
    fields = ['name', 'description', 'price']

    # Override the form_valid method
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TrackingDetails
    fields = ['target_price']

    # Override the form_valid method
    def form_valid(self, form):
        form.instance.user = self.request.user
        #Redirect to item detail view
        tracking_details = self.get_object()
        self.success_url = '/item/' + str(tracking_details.pk) + '/'
        return super().form_valid(form)


    # Makes sure only the creator of a specific item can update it
    def test_func(self):
        user = self.get_object().user  # Gets exact item were updating
        # Check to make sure current user is author of item
        if self.request.user == user:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/'  # If the deletion is successful, redirect to homepage

    # Makes sure only the author of a specific post can update it. Overrides test_func method
    def test_func(self):
        item = self.get_object()  # Gets exact item were deleting
        # Check to make sure current user is author of item
        if self.request.user == item.user:
            return True
        return False


class ItemListView(ListView):
    model = TrackingDetails
    context_object_name = 'tracking_details'
    template_name = 'item_searcher/list.html'


def help(request):
    return HttpResponse('<h1>Help</h1>')
