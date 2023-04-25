from django.contrib import admin
from .models import *


class ProductAdmion(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}





class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}




admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmion)

admin.site.register(CartItem)
admin.site.register(Cart)

admin.site.register(Order)
