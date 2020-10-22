from django.shortcuts import render
from .models import Product, Order, OrderItem
from django.http import JsonResponse
import json
from django.db.models import Q


def get_context(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.prefetch_related('order_items').get_or_create(customer=customer, is_complete=False)
        items = order.order_items.select_related('product').all()
        cart_items_amount = order.cart_items_amount
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            print('CART:', cart)
        items = []
        order = {'cart_total': 0, 'cart_items_amount': 0}
        cart_items_amount = order['cart_items_amount']
        for item in cart:
            cart_items_amount += cart[item]['quantity']
            product = Product.objects.get(id=item)
            total = product.price * cart[item]['quantity']
            order['cart_total'] += total
            order['cart_items_amount'] += cart[item]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url,
                    'category': product.category,
                    'description': product.description
                },
                'quantity': cart[item]['quantity'],
                'total': total,
            }
            items.append(item)


    context = {'items': items, 'order': order, 'cart_items_amount': cart_items_amount}
    return context


def store(request):
    search = request.GET.get('search', '')
    order_by = request.GET.get('order_by')
    if search and order_by == 'Price':
        products = Product.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search) | Q(id__icontains=search)).order_by('price')
    elif search and order_by == 'Id':
        products = Product.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search) | Q(id__icontains=search)).order_by('id')
    elif search and order_by == 'Name':
        products = Product.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search) | Q(id__icontains=search)).order_by('name')
    elif search and order_by == 'Order by':
        products = Product.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search) | Q(id__icontains=search))
    else:
        products = Product.objects.raw(
        'SELECT id, name, description, price, image FROM store_product')

    context = get_context(request)
    context['products'] = products
    return render(request, "store.html", context)


def cart(request):
    context = get_context(request)
    return render(request, "cart.html", context)


def checkout(request):
    context = get_context(request)
    return render(request, "checkout.html", context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        customer=customer, is_complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)