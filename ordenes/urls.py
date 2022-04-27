

from django.urls import path
from .views import Home, ItemDetail, add_item


ordenes_patterns = ([
    path('', Home.as_view(), name='home'),
    path('item/<slug>/', ItemDetail.as_view(), name='item_detail'),
    path('add_item/<slug>/', add_item, name='add-item'),
], 'ordenes')