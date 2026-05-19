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
    path('api/products/', views.ProductListCreateAPIView.as_view(), name='product_api'),
    path('api/products/<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_detail_api'),
    path('api/vendor/products/', views.VendorProductListAPIView.as_view(), name='vendor_products'),
    path('api/admin/products/', views.AdminProductListAPIView.as_view(), name='admin_products'),
    path('api/vendor/brand/', views.VendorBrandUpdateAPIView.as_view(), name='vendor_brand_update'),
    path('api/vendor/dashboard/', views.VendorDashboardAPIView.as_view(), name='vendor_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/vendor-approval/<int:vendor_id>/', views.vendor_approval, name='vendor_approval'),
    path('dashboard/vendor/', views.vendor_dashboard_page, name='vendor_dashboard_page'),
    path('api/categories/', views.CategoryListCreateAPIView.as_view(), name='category_list_create_api'),
    path('api/categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category_detail_api'),
    path('api/brands/', views.BrandListCreateAPIView.as_view(), name='brand_list_create_api'),
    path('api/brands/<int:pk>/', views.BrandRetrieveUpdateDestroyAPIView.as_view(), name='brand_detail_api'),
    path('api/orders/', views.OrderListCreateAPIView.as_view(), name='order_list_create_api'),
    path('api/orders/<int:pk>/', views.OrderRetrieveAPIView.as_view(), name='order_detail_api'),
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
