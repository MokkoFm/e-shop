from django.contrib import admin
from store.models import Customer, ProductCategory, Product, Order, OrderItem

admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(Product)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'registrated_at', 'is_complete', 'transaction_id']
    inlines = [OrderItemInline]
