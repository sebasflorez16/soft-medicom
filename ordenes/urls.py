

from django.urls import path
from .views import AddCouponView, ItemDetail, add_item, OrderSummaryView, remove_from_cart, remove_single_item_from_cart, AddCouponView, CheckoutView
                

ordenes_patterns = ([
    #path('', ItemList.as_view(), name='item-list'),
    path('order_summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('item/<slug>/', ItemDetail.as_view(), name='item_detail'),
    path('add_item/<slug>/', add_item, name='add-item'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart,
            name = 'remove-single-item-from-cart' ),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon')
], 'ordenes')