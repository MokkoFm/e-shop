from django.contrib import admin
from store.models import Customer, ProductCategory, Product, Order, OrderItem

# Register your models here.
admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
