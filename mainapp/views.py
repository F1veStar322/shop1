from .models import Product, Category, Cart, CartItem
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render ,redirect ,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View , CreateView
from django.contrib.auth.views import LoginView

from django.contrib import messages

from .forms import OrderForm , RegisterUserForm , LoginUserForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import CartMixin

from django.core.paginator import Paginator


class BaseView( View):
    def get(self, request, *args, **kwargs):

        category_list = Category.objects.filter(is_available=True)

        paginator = Paginator(category_list, 4)

        page = request.GET.get('page')

        categories = paginator.get_page(page)

        products = Product.objects.filter(is_available=True)

        context = {
            'categories': categories,
            'products': products,
        }
        return render(request, 'index.html', context)


def show_category(request, slug):

    category = get_object_or_404(Category, slug=slug)

    category_list = Category.objects.filter(is_available=True)

    paginator = Paginator(category_list, 4)

    page = request.GET.get('page')

    categories = paginator.get_page(page)

    products = Product.objects.filter(category=category, is_available=True)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }

    return render(request, 'category_detail.html', context )






@login_required
def view_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.price * item.qty for item in cart_items)
    total_s = total-150
    context = {
        'cart_items': cart_items,
        'total': total,
        'total_s':total_s

    }
    return render(request, 'cart.html', context)



class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)

        cart_item, created = CartItem.objects.get_or_create(cart=self.cart, product=product)

        if product.sale == True:
            cart_item.price = product.new_price
        else:
            cart_item.price = product.price

        cart_item.save()
        messages.add_message(request, messages.INFO, "Товар успішно добавлений")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)

        cart_item = CartItem.objects.get(cart=self.cart, product=product)

        cart_item.delete()

        messages.add_message(request, messages.INFO, "Товар успішно видалено")
        return HttpResponseRedirect('/cart/')



class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)

        cart_item = CartItem.objects.get(product=product, cart=self.cart)

        qty = int(request.POST.get('qty'))
        cart_item.qty = int(qty)
        cart_item.save()
        messages.add_message(request, messages.INFO, "К-сть успішно змінено")
        return HttpResponseRedirect('/cart/')



class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        total = sum(item.price * item.qty for item in self.cart_items)
        context = {
            'cart': self.cart,
            'cart_items': self.cart_items,
            'form': form,
            'total' : total
        }
        return render(request, 'checkout.html', context)






class MakeOrderView(CartMixin,LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = self.user
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.eaddress = form.cleaned_data['eaddress']
            # new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.state = form.cleaned_data['state']
            new_order.number_nova_post = form.cleaned_data['number_nova_post']
            new_order.save()
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            messages.add_message(request, messages.INFO, 'Дякую за замовлення! Менеджер звяжеться з вами!')
            return HttpResponseRedirect('https://pay.fondy.eu/s/B7tRm8Z5AKL4')
        return HttpResponseRedirect('/checkout/')





class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('base')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('base')


def logout_user(request):
    logout(request)
    return redirect('login')








