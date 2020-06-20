#This contains all the urls specific to this item_searcher app
from django.urls import path
from .views import ItemSearchView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView
from . import views

urlpatterns = [
    path('', ItemSearchView.as_view(), name='item_searcher_home'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_searcher_detail'), #By specifying the pk variable in the url, it allows us to grab that value and use it in our view function
    path('item/<int:pk>/update', ItemUpdateView.as_view(), name='item_searcher_update'),
    path('item/<int:pk>/delete', ItemDeleteView.as_view(), name='item_searcher_delete'),
    path('item/new/', ItemCreateView.as_view(), name='item_searcher_create'),
    path('about/', views.about, name='item_searcher_about'),
    path('help/', views.help, name='item_searcher_help'),
]


