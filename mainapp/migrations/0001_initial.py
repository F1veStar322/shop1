# Generated by Django 4.1.7 on 2023-04-21 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='назва категорії')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='фото')),
                ('slug', models.SlugField(unique=True)),
                ('is_available', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва(смак)')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=2000, verbose_name='опис')),
                ('image', models.ImageField(upload_to='', verbose_name='фото')),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('is_available', models.BooleanField(default=True)),
                ('sale', models.BooleanField(verbose_name='знижка')),
                ('new_price', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('new', models.BooleanField(default=False, verbose_name='новинка')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категорія')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Імя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Прізвище')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('eaddress', models.CharField(max_length=1024, verbose_name='електронна пошта')),
                ('state', models.CharField(max_length=111, verbose_name='область/місто')),
                ('number_nova_post', models.CharField(max_length=111, verbose_name='віділення нової пошти')),
                ('status', models.CharField(choices=[('new', 'Нове замовлення'), ('in_progress', 'Замовлення на опрацюванні'), ('is_ready', 'Замовлення готове'), ('completed', 'Замовлення виконано')], default='new', max_length=100, verbose_name='Статус замовлення')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комент до замовлення')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')),
                ('order_date', models.DateField(default=django.utils.timezone.now, null=True, verbose_name='Дата отримання замовлення')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.cart', verbose_name='Корзина')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_orders', to=settings.AUTH_USER_MODEL, verbose_name='Клієнт')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10, null=True)),
                ('final_price', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='Загальна ціна')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
            ],
        ),
    ]
