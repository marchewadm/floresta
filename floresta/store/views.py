import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import *


def get_message(request):
    message = request.session.pop('message', None)
    return {'message': message}


def index(request):
    products = Product.objects.filter(new__exact=True)
    context = {'products': products}
    context.update(get_message(request))
    return render(request, 'store/index.html', context)


def store(request, page=1, category_name="all"):
    def paginate(paginator, page, current_category_fullname):
        page = request.GET.get('page', page)
        all_products = paginator.get_page(page)
        all_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
        return {'products': all_products, 'current_category_fullname': current_category_fullname}

    if category_name == "all":
        paginator = Paginator(Product.objects.all(), 20)
        context = paginate(paginator, page, 'Wszystkie rośliny')
    elif category_name == "new":
        paginator = Paginator(Product.objects.filter(new__exact=True), 20)
        context = paginate(paginator, page, 'Nowości')
    else:
        category_obj = get_object_or_404(ProductCategory, slug=category_name)
        paginator = Paginator(Product.objects.filter(category=category_obj), 20)
        context = paginate(paginator, page, category_obj.name)

    categories = ProductCategory.objects.all()
    context.update({'categories': categories, 'current_category': category_name})
    context.update(get_message(request))
    return render(request, 'store/store.html', context)


def product(request, product_name, product_id):
    product_obj = get_object_or_404(Product, id=product_id)

    context = {'product_obj': product_obj}
    context.update(get_message(request))
    return render(request, 'store/product.html', context)


def cart(request):
    if not request.user.is_authenticated:
        request.session['message'] = "Musisz być zalogowany, aby móc wykonać tę czynność"
        return redirect('/signin/')

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    context = {'items': items, 'order': order, 'shippers': Shipper.objects.all()}
    context.update(get_message(request))
    return render(request, 'store/cart.html', context)


def checkout(request):
    if not request.user.is_authenticated:
        request.session['message'] = "Musisz być zalogowany, aby móc wykonać tę czynność"
        return redirect('/signin/')

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    # Check if the cart is empty, and if it is, return to the cart immediately.
    if not items:
        request.session['message'] = 'Koszyk nie może być pusty'
        return redirect('/cart/')

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    if not request.user.is_authenticated:
        request.session['message'] = "Musisz być zalogowany, aby móc wykonać tę czynność"
        return JsonResponse({'error': 'Authentication required'})

    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    current_url = data['currentUrl']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "increase":
        order_item.quantity += 1
        current_url_list = current_url.split("/")
        # Inform the user about the product being added to the cart when the user is not inspecting the cart.
        if "cart" not in current_url_list:
            request.session['message'] = "Produkt został dodany do koszyka"
    elif action == "decrease":
        order_item.quantity -= 1
    elif action == "remove":
        order_item.quantity = 0
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)
