from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone






class Category(models.Model):

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=255, verbose_name='назва категорії')
    image = models.ImageField(verbose_name='фото', blank=True)
    slug = models.SlugField(unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Назва(смак)')
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=2000 , verbose_name='опис')
    image = models.ImageField(verbose_name='фото')
    price = models.DecimalField(max_digits=10, decimal_places=0,)
    is_available = models.BooleanField(default=True)
    sale = models.BooleanField(verbose_name='знижка')
    new_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    new = models.BooleanField(default=False, verbose_name='новинка')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # products = models.ManyToManyField('CartItem', blank=True)



class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    final_price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Загальна ціна')

    def save(self, *args, **kwargs):
        if self.product.sale == True:
            price = self.product.new_price
        else:
            price = self.product.price

        self.final_price = self.qty * price
        super().save(*args, **kwargs)




class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення на опрацюванні'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконано')
    )

    # BUYING_TYPE_CHOICES = (
    #     (BUYING_TYPE_SELF, 'Самовивіз'),
    #     (BUYING_TYPE_DELIVERY, 'Доставка')
    # )

    customer = models.ForeignKey(User, verbose_name='Клієнт',related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Імя')
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE , null=True)
    eaddress = models.CharField(max_length=1024, verbose_name='електронна пошта')
    state = models.CharField(max_length=111 , verbose_name='область/місто')
    number_nova_post = models.CharField(max_length=111, verbose_name='віділення нової пошти')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    # buying_type = models.CharField(
    #     max_length=100,
    #     verbose_name='Тип замовлення',
    #     choices=BUYING_TYPE_CHOICES,
    #     default=BUYING_TYPE_SELF
    # )
    comment = models.TextField(verbose_name='Комент до замовлення', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')
    order_date = models.DateField(verbose_name='Дата отримання замовлення', default=timezone.now, null=True)

    def __str__(self):
        return str(self.id)


