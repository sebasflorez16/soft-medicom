from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.utils.timezone import timezone



from core.models import Pacientes

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Items(models.Model):
    item = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField()
    discount_price = models.FloatField(blank=True, null=True)  # el precio que esta tachado en el template
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return self.item

    def get_absolute_url(self):
        return reverse("ordenes:item_detail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self): #Crea una url absoluta. se importa desde la vista para ponerla en el template y añada los productos al carrito
        return reverse("ordenes:add-item", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price()

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(Items)
    quantity = models.IntegerField(default=1)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username




class Checkout(models.Model):
    client = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    items = models.ManyToManyField(Items)

    def __str__(self):
        return self.client


