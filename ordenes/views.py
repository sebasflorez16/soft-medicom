from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect

from .models import Items, OrderItem,  Order, Coupon

from .forms import CouponForm, CheckoutForm


# Create your views here.

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            form = CheckoutForm(self.request.POST)
            context={
                'form':form,
                'couponform': CouponForm(),
                'order':order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, 'ordenes/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "No tienes una orden activa")
            return redirect(self.request, 'ordenes:order-summary')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                order.save()
                return render(self.request, 'ordenes/checkout.html')
        except ObjectDoesNotExist:
            messages.info(self.request, 'No tienes una orden activa')
            return redirect('ordenes:order-summary')


class ItemDetail(DetailView):
    model = Items
    template_name = 'ordenes/item.html'


"""class ItemList(View):
    template_name = 'ordenes/order-summary.html'
    model = Items
    paginate_by = 10
    object_context_name = "items"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Items.objects.all()
        return context"""

# class CheckiutView(TemplateView):

class OrderSummaryView(LoginRequiredMixin, ListView):
    template_name = 'ordenes/order-summary.html'
    model = Order
    model2 = Items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = Order.objects.get(user=self.request.user, ordered=False)
        context["items"] = Items.objects.all()
        return context
    



    """def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            item = Items.objects.all()
            context = {
                'object': order,
                'item': item
            }
            print("hola desde consola")
            return render(self.request, 'ordenes/order-summary.html', context)
            
        except ObjectDoesNotExist:
            messages.warning(self.request, "No tienes un pedido activo")
            return redirect("ordenes:item-list")

"""
# Vamos a crear la funcion para activarla desde el modelo por un url_direct


def add_item(request, slug):
    item  = get_object_or_404(Items, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user=request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'El item fue añadido o actualizado')
            return redirect("ordenes:order-summary")
            
        else:
            order.items.add(order_item)
            messages.error(request, 'Un error ha ocurrido')
            return redirect("ordenes:order-summary")
    
    else:
        ordered_date = timezone.now
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "se ha creado la order")
        return redirect("ordenes:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        #Verifica si ha una OrderItem dentro de la Order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "El item fue removido de la orden")
            return redirect("ordenes:order-summary")
        else:
            messages.info(request, "El item no estaba en esta lista")
            return redirect("ordenes:item-list", slug=slug)
    else:
        messages.info(request, "No tienes una orden activa en este momento", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        #Verifica si ha una OrderItem dentro de la Order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                messages.info(request, "La cantidad del item fue actualizada")
                return redirect("ordenes:order-summary")
        else:
            messages.info(request, "El item no estaba en la orden")
            return redirect("ordenes:order-summary", slug=slug)
    else:
        messages.info(request, "No tienes una orden activa")
        return redirect("ordenes:order-summary", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.warning("El cupon no existe")
        return redirect("ordenes:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None) #Valida que el metodo de la plantilla sea POST
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user,
                    ordered = False
                )

                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Se ha agregado el cupon. ¡Es valido!")
                return redirect("ordenes:checkout")
            except ObjectDoesNotExist:
                messages.warning(self.request, "El cupon no existe")
                return 





"""def add_item(request, slug):
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
"""