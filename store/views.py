from django.shortcuts import render
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


def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def product(request):
    context = {}
    return render(request, 'store/product.html', context)


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)
