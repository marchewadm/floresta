from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('store/', views.store, name='store'),
    path('store/<int:page>', views.store, name='store'),
    path('product/<str:product_name>/<int:product_id>', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateitem/', views.update_item, name='updateitem')
]
