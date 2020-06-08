#This contains all the urls specific to this item_searcher app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='item_searcher_home'),
    path('about/', views.about, name='item_searcher_about'),
    path('help/', views.help, name='item_searcher_help'),
]