from django.shortcuts import render
from .models import Product


def store(request):
    products = Product.objects.raw('SELECT * FROM store_product')
    context = {'products': products}
    return render(request, "store.html", context)


def cart(request):
    context = {}
    return render(request, "cart.html", context)


def checkout(request):
    context = {}
    return render(request, "checkout.html", context)
