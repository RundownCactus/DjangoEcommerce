from django.urls import path
from .views import HomeView
from .views import ItemDetailView
from .views import checkout
from .views import product
from .views import add_to_cart
from .views import remove_from_cart
from .views import OrderSummaryView
from .views import SearchHomeView
from .views import search
from .views import Tracker

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkout, name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/', product, name='product'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('search/', search, name='search'),
    path('Tracker/', Tracker, name='Tracker'),

]
