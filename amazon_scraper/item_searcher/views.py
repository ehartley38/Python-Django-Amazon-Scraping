from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView, ListView

from . import site_scraper
from .forms import ItemSearchForm, ItemTrackingForm, ItemTestForm
from .models import Item, TrackingDetails, Price
from . import tasks
from datetime import datetime


'''Return True if the item input is already in the database'''

def is_duplicate(url):
    for item in Item.objects.all():
        if item.url == url:
            return True
    return False

'''Return True if player is already tracking the item'''

def user_already_tracks(url, user):
    for tracker in TrackingDetails.objects.all():
        if (tracker.user == user) and (tracker.item.url == url):
            return True
    return False


class ItemSearchView(FormView):
    template_name = 'item_searcher/home.html'  # <app>/<model>_<viewtype>.html
    form_class = ItemSearchForm

    def form_valid(self, form):
        url = form.cleaned_data.get('url')
        product = site_scraper.gather_info(url)
        #If item is already in database
        if is_duplicate(url):
            if user_already_tracks(url, self.request.user):
                print('You are already tracking this item!')
                self.success_url = '/'
                return super().form_valid(form)
            item = Item.objects.get(url=url)
            self.success_url = 'trackinginfo/' + str(item.pk) + '/'
        else:
            item = Item.objects.create(name=product.title, current_price=product.price, url=url)
            self.success_url = 'trackinginfo/' + str(item.pk) + '/'

        tasks.update_pricing_info()
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
        target_price = form.cleaned_data.get('target_price')
        item = self.get_context_data()['item']
        price = Price.objects.create(item=item, price=item.current_price, date=datetime.now().date())
        tracking_info = TrackingDetails.objects.create(target_price=target_price,
                                                       user=self.request.user, item=item)
        item.save()
        price.save()
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
    model = TrackingDetails
    success_url = '/'  # If the deletion is successful, redirect to homepage

    # Makes sure only the author of a specific post can update it. Overrides test_func method
    def test_func(self):
        tracking_details = self.get_object()  # Gets exact item were deleting
        # Check to make sure current user is author of item
        if self.request.user == tracking_details.user:
            return True
        return False


class ItemListView(ListView):
    model = TrackingDetails
    context_object_name = 'tracking_details'
    template_name = 'item_searcher/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_items'] = TrackingDetails.objects.all().filter(user=self.request.user)
        return context


class ItemTestView(FormView):
    template_name = 'item_searcher/test_page.html'
    form_class = ItemTestForm
    success_url = '/testing/'

    def form_valid(self, form):
        tasks.update_pricing_info()

        for price in Price.objects.all():
            print(price.date.date())



        return super().form_valid(form)