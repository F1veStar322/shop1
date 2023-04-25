from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cart , CartItem , Product, Category






class CartMixin(LoginRequiredMixin,View):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            cart = Cart.objects.create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        self.user = user
        self.cart_items = cart_items
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)

