from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from django.contrib import messages

from .models import Items, OrderItem, Order, Checkout, UserProfile


# Create your views here.


class ItemDetail(DetailView):
    model = Items
    template_name = 'ordenes/item.html'


class Home(ListView):
    template_name = 'ordenes/ordenes.html'
    model = Items
    paginate_by = 10

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Items.objects.all()
        return context


# class CheckiutView(TemplateView):

class OrderSummaryView(LoginRequiredMixin, ListView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'ordenes/ordenes.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "No tienes un pedido activo")
            return redirect("ordenes:ordenes")


# Vamos a crear la funcion para activarla desde el modelo por un url_direct
def add_item(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_item, create = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        # verifica si el item esta en la orden que ya estaba o la que fue creada
        if order.items.filter(slug__iexact=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Los articulos han sido actualizados en el carrito")
            return redirect("ordenes:home")
        else:
            order.items.add(order_item)
            messages.info(request, "Este articulo fue añadido al carrito de compras")
            return redirect("ordenes:home")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Este articulo ya fue añadido al carrito")
        return redirect("ordenes:home")
