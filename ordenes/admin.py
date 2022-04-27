from django.contrib import admin
from .models import Items,  OrderItem, Order, Coupon
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    model = Items
    list_display = ['item', 'price', 'description']





class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['user',
                    'ordered',
                    'payment',
                    'coupon',
                    #'start_date'
                    ]


#Verificar si necesitamos el Modelo de Checkout en el admin

admin.site.register(Items, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)

