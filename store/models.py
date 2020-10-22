from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200)
    user = models.OneToOneField(
        User, blank=True, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="category")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products',
        verbose_name="category")
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="price")
    image = models.ImageField(upload_to="pizzas", verbose_name="image")
    description = models.TextField(blank=True, verbose_name="description")

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name='orders', verbose_name="customer")
    registrated_at = models.DateTimeField(
        default=timezone.now, verbose_name='registration time of order')
    is_complete = models.BooleanField(
        default=False, db_index=True, verbose_name="status")
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f" Order number - {self.id}"

    @property
    def cart_total(self):
        return sum([item.total for item in self.order_items.all()])

    @property
    def cart_items_amount(self):
        return sum([item.quantity for item in self.order_items.all()])

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True,
        related_name='product_items', verbose_name='product_items')
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True,
        related_name='order_items', verbose_name='order_items')
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(25)],
        verbose_name='quantity', default=0)

    def __str__(self):
        return f"{self.product}: {self.quantity}"

    @property
    def total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "order item"
        verbose_name_plural = "order items"
