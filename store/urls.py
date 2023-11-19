from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('store/', lambda request: redirect('category/all'), name="store"),
    path('store/category/<str:category_name>/', views.store, name="store_category"),
    path('store/category/<str:category_name>/<int:page>/', views.store, name="store_category_page"),
    path('product/<str:product_name>/<int:product_id>/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateitem/', views.update_item, name='updateitem')
]
