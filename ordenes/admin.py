from django.contrib import admin
from .models import Items, Order, Checkout, OrderItem
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    model = Items
    list_display = ['item', 'price', 'description']



class OrderAdmin(admin.ModelAdmin):
    model = Order

    class OrderAdmin(admin.ModelAdmin):
        list_display = ['user',
                        'ordered',
                        'payment',
                        'coupon',
                        #'start_date'
                        ]


#Verificar si necesitamos el Modelo de Checkout en el admin

admin.site.register(Items)
admin.site.register(OrderItem)
admin.site.register(Order)

