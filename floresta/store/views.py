import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import *
from .forms import CartForm, CheckoutForm


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
    order, created = Order.objects.get_or_create(customer=customer, is_paid=False)
    items = order.orderitem_set.all()

    # Retrieving the previous selection data for the shipper and comment if the user navigated back to the cart
    # after submitting the form.
    prev_shipper_id = order.shipper.id if order.shipper else None
    prev_order_comment = order.comment if order.comment else ""

    # Form initialization
    form = CartForm(request.POST or None, initial={'shipper': prev_shipper_id, 'order_comment': prev_order_comment})
    form.fields['shipper'].choices = [
        ('', 'Wybierz formę dostawy')
    ] + [
        (shipper.id, f"{shipper.name} - {shipper.price:.2f} zł") for shipper in Shipper.objects.all()
    ]

    if request.method == "POST" and form.is_valid():
        # Check if the cart is empty, and if it is, return to the cart immediately.
        if not items:
            request.session['message'] = 'Koszyk nie może być pusty'
            return redirect('/cart/')

        shipper_id = form.cleaned_data['shipper']
        order_comment = form.cleaned_data['order_comment']

        if order_comment:
            order.comment = order_comment
        else:
            order.comment = ""

        if shipper_id:
            shipper = get_object_or_404(Shipper, id=shipper_id)
            order.shipper = shipper

        order.save()
        return redirect('/checkout/')

    context = {'items': items, 'order': order, 'form': form}
    context.update(get_message(request))
    return render(request, 'store/cart.html', context)


def checkout(request):
    if not request.user.is_authenticated:
        request.session['message'] = "Musisz być zalogowany, aby móc wykonać tę czynność"
        return redirect('/signin/')

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, is_paid=False)
    items = order.orderitem_set.all()

    # Check if the cart is empty, and if it is, return to the cart immediately.
    if not items:
        request.session['message'] = 'Koszyk nie może być pusty'
        return redirect('/cart/')

    form = CheckoutForm(
        request.POST or None,
        initial={'first_name': customer.name.capitalize(), 'email': customer.email}
    )

    if request.method == "POST" and form.is_valid():
        shipping_address, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)

        for field in ['name', 'last_name', 'email', 'street', 'city', 'postal_code']:
            setattr(shipping_address, field, form.cleaned_data[field])
        if form.cleaned_data['phone_number']:
            shipping_address.phone = form.cleaned_data['phone_number']
        shipping_address.save()

        # Change total_quantity in Product model when product is purchased
        for item in items:
            product = item.product
            quantity = item.quantity

            product.total_quantity -= quantity
            product.save()

        order.is_paid = True
        order.total = order.get_total_price
        order.save()

        request.session['message'] = "Zamówienie zostało złożone"
        return redirect("/")

    context = {'items': items, 'order': order, 'form': form}
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
    order, created = Order.objects.get_or_create(customer=customer, is_paid=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "increase":
        if order_item.quantity < product.total_quantity:
            order_item.quantity += 1
            current_url_list = current_url.split("/")
            # Inform the user about the product being added to the cart when the user is not inspecting the cart.
            if "cart" not in current_url_list:
                request.session['message'] = "Produkt został dodany do koszyka"
        else:
            request.session['message'] = "Aktualnie nie posiadamy tylu sztuk wybranego produktu"
    elif action == "decrease":
        order_item.quantity -= 1
    elif action == "remove":
        order_item.quantity = 0
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)
