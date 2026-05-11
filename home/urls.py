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

    # Contact
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
#     path('products/', views.product_list, name='product_list'),
    path('api/products/', views.product_api, name='product_api'),
    path('api/product/<int:id>/', views.product_detail_api),
    path('api/categories/', views.category_api),
    path('api/brands/', views.brand_api),
    path('api/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('api/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('api/view-cart/', views.view_cart, name='view_cart'),
    path('api/place-order/', views.place_order, name='place_order'),
    path('api/my-orders/', views.my_orders, name='my_orders'),

    path('api/create-product/', views.create_product, name='create_product'),

    path('api/update-product/<int:id>/', views.update_product, name='update_product'),

    path('api/delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('api/search/', views.search_product, name='search_product'),

    path('api/category-products/<int:id>/', views.category_products, name='category_products'),

    path('api/brand-products/<int:id>/', views.brand_products, name='brand_products'),

    path('api/cart-total/', views.cart_total, name='cart_total'),

    path('api/increment-cart/', views.increment_cart, name='increment_cart'),

    path('api/decrement-cart/', views.decrement_cart, name='decrement_cart'),

]
