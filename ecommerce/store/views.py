from django.shortcuts import render
from .models import Product, Order, User


def store(request):
    products = Product.objects.raw('SELECT * FROM store_product')
    context = {'products': products}
    return render(request, "store.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
        items = order.order_items.all()
    else:
        items = []
        order = {'cart_total': 0, 'cart_items_amount': 0}

    context = {'items': items, 'order': order}
    return render(request, "cart.html", context)


def checkout(request):
    context = {}
    return render(request, "checkout.html", context)
