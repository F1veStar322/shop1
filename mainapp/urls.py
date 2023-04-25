from django.urls import path
from .views import (
    BaseView,
    show_category,
    view_cart,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CheckoutView,
    MakeOrderView,
    LoginUser,
    logout_user,
    RegisterUser
)


urlpatterns = [

    path('', BaseView.as_view(), name='base'),
    path('category/<str:slug>/', show_category, name='category_detail'),


    path('cart/', view_cart, name='cart'),
    path('cart/add/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<str:slug>/', DeleteFromCartView.as_view(), name='remove_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

]


