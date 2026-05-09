from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("signup/", views.signup, name='signup'),
    path("accounts/", include('django.contrib.auth.urls')),

    # Add to Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

    # contact

    path('contact_us', views.Contact_Page, name="contact_page"),
    # Check Out
    path('checkout/', views.checkout, name="checkout"),

    # Order
    path('order/', views.Your_Order, name="your_order"),
    # Product
    path('product/', views.Product_page, name='product'),
    # Product Detail
    path('detail/<str:id>', views.product_detail, name='product_detail'),
    # Search
    path('search/', views.Search,name='search'),
]
