import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import *


def index(request):
    products = Product.objects.filter(new__exact=True)
    context = {'products': products}
    return render(request, 'store/index.html', context)


def signin(request):
    context = {}
    return render(request, 'store/signin.html', context)


def signup(request):
    context = {}
    return render(request, 'store/signup.html', context)


def store(request, page=1):
    paginator = Paginator(Product.objects.all(), 20)
    page = request.GET.get("page", page)
    products = paginator.get_page(page)
    products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    context = {'products': products}
    return render(request, 'store/store.html', context)


def product(request, product_name, product_id):
    product_obj = get_object_or_404(Product, id=product_id)

    context = {'product_obj': product_obj}
    return render(request, 'store/product.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order, 'shippers': Shipper.objects.all()}
    return render(request, 'store/cart.html', context)


def checkout(request):
    # context = {}
    # return render(request, 'store/checkout.html', context)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print(f"Action: {action}")
    print(f"ProductID: {product_id}")

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "increase":
        order_item.quantity += 1
    elif action == "decrease":
        order_item.quantity -= 1
    elif action == "remove":
        order_item.quantity = 0
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)
