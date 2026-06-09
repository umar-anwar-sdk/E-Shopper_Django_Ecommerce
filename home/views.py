from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.db.models import Q
from django.conf import settings
from rest_framework import generics, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.decorators import admin_required, vendor_required
from authentication.permissions import (
    IsAdminUserRole,
    IsVendorUserRole,
    IsCustomerUserRole,
    IsAdminOrVendor,
    IsOwnerOrAdmin,
    IsVendorProductOwner,
)
from home.models import Category, Product, Order, Brand, Slider, Contact_us, UserCreateForm
from cart.cart import Cart
from .serializers import CategorySerializer, ProductSerializer, BrandSerializer, OrderSerializer

User = get_user_model()


# ----------------------------- API Helpers -----------------------------

def _get_product(product_id):
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None


def _serialize_errors(serializer):
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------- API Views -----------------------------

@api_view(['GET'])
def product_api(request):
    products = Product.objects.select_related('brand', 'Category', 'vendor').all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail_api(request, id):
    product = _get_product(id)
    if not product:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    product = _get_product(product_id)
    if not product:
        return Response({'error': 'Invalid product id'}, status=status.HTTP_404_NOT_FOUND)

    cart = request.session.get(settings.CART_SESSION_ID, {})
    product_id = str(product.id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'image': product.image.url if product.image else ''
        }

    request.session[settings.CART_SESSION_ID] = cart
    request.session.modified = True

    return Response({'message': 'Product added to cart', 'cart': cart})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    return Response(cart)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    product_id = str(request.data.get('product_id'))
    cart = request.session.get(settings.CART_SESSION_ID, {})

    if product_id in cart:
        del cart[product_id]
        request.session[settings.CART_SESSION_ID] = cart

    return Response({'message': 'Removed', 'cart': cart})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    if not cart:
        return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

    for item in cart.values():
        total = item['price'] * item['quantity']
        Order.objects.create(
            user=request.user,
            product=item['name'],
            price=item['price'],
            quantity=item['quantity'],
            image=item.get('image', ''),
            address=request.data.get('address', ''),
            phone=request.data.get('phone', ''),
            pincode=request.data.get('pincode', ''),
            total=total,
        )

    request.session[settings.CART_SESSION_ID] = {}
    request.session.modified = True

    return Response({'message': 'Order placed successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    product = _get_product(id)
    if not product:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.is_vendor() and product.vendor != request.user:
        return Response({'error': 'You may only update your own products.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return _serialize_errors(serializer)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    product = _get_product(id)
    if not product:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.is_vendor() and product.vendor != request.user:
        return Response({'error': 'You may only delete your own products.'}, status=status.HTTP_403_FORBIDDEN)

    product.delete()
    return Response({'message': 'Product deleted'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    if not (request.user.is_vendor() or request.user.is_admin()):
        return Response({'error': 'You do not have permission to add products.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        if request.user.is_vendor():
            serializer.save(vendor=request.user)
        else:
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return _serialize_errors(serializer)


@api_view(['GET'])
def search_product(request):
    keyword = request.GET.get('keyword', '')
    products = Product.objects.filter(
        Q(name__icontains=keyword) |
        Q(details__icontains=keyword) |
        Q(brand__name__icontains=keyword) |
        Q(Category__name__icontains=keyword)
    ).distinct()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_products(request, id):
    products = Product.objects.filter(Category=id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def brand_products(request, id):
    products = Product.objects.filter(brand=id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_total(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return Response({'total': total})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increment_cart(request):
    product_id = str(request.data.get('product_id'))
    cart = request.session.get(settings.CART_SESSION_ID, {})

    if product_id not in cart:
        return Response({'error': 'Product not in cart'}, status=status.HTTP_404_NOT_FOUND)

    cart[product_id]['quantity'] += 1
    request.session[settings.CART_SESSION_ID] = cart
    request.session.modified = True
    return Response({'message': 'Quantity increased', 'cart': cart})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrement_cart(request):
    product_id = str(request.data.get('product_id'))
    cart = request.session.get(settings.CART_SESSION_ID, {})

    if product_id not in cart:
        return Response({'error': 'Product not in cart'}, status=status.HTTP_404_NOT_FOUND)

    cart[product_id]['quantity'] -= 1
    if cart[product_id]['quantity'] <= 0:
        del cart[product_id]
    request.session[settings.CART_SESSION_ID] = cart
    request.session.modified = True
    return Response({'message': 'Quantity decreased', 'cart': cart})


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """List products for everyone and allow admins/vendors to create products."""
    queryset = Product.objects.select_related('brand', 'Category', 'vendor').order_by('-id').all()
    serializer_class = ProductSerializer
    pagination_class = None

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrVendor()]

    def perform_create(self, serializer):
        if self.request.user.is_vendor():
            serializer.save(vendor=self.request.user)
            return

        if self.request.user.is_admin():
            vendor = serializer.validated_data.get('vendor')
            serializer.save(vendor=vendor or self.request.user)
            return

        raise permissions.PermissionDenied('You do not have permission to add products.')


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve a product for anyone and allow owners/admins to update or delete."""
    queryset = Product.objects.select_related('brand', 'Category', 'vendor').all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsVendorProductOwner()]

    def perform_update(self, serializer):
        if self.request.user.is_vendor() and serializer.instance.vendor != self.request.user:
            raise permissions.PermissionDenied('You may only update your own products.')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.is_vendor() and instance.vendor != self.request.user:
            raise permissions.PermissionDenied('You may only delete your own products.')
        instance.delete()


class VendorProductListAPIView(generics.ListAPIView):
    """List products that belong to the current vendor."""
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsVendorUserRole]
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user).select_related('brand', 'Category')


class AdminProductListAPIView(generics.ListAPIView):
    """Admin view of all products."""
    queryset = Product.objects.select_related('brand', 'Category', 'vendor').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = None


class VendorBrandUpdateAPIView(generics.UpdateAPIView):
    """Allow a vendor to update branding and banner assets."""
    permission_classes = [IsAuthenticated, IsVendorUserRole]

    def get_serializer_class(self):
        from authentication.serializers import UpdateProfileSerializer
        return UpdateProfileSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """List categories for everyone and allow admin to create categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUserRole()]


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]


class BrandListCreateAPIView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = None

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUserRole()]


class BrandRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]


class OrderListCreateAPIView(generics.ListCreateAPIView):
    """List orders for current user and allow customers to place orders."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin():
            return Order.objects.all().select_related('user')
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    """Retrieve a single order for owner or admin."""
    queryset = Order.objects.select_related('user').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class VendorDashboardAPIView(generics.RetrieveAPIView):
    """Vendor dashboard with product counts and ownership stats."""
    permission_classes = [IsAuthenticated, IsVendorUserRole]

    def get(self, request, *args, **kwargs):
        total_products = Product.objects.filter(vendor=request.user).count()
        total_brands = Brand.objects.filter(product__vendor=request.user).distinct().count()
        return Response({
            'vendor_id': request.user.id,
            'vendor_email': request.user.email,
            'shop_name': request.user.shop_name,
            'total_products': total_products,
            'total_brands': total_brands,
            'active': True,
        })


# ----------------------------- Template Views -----------------------------

@admin_required
def admin_dashboard(request):
    total_customers = User.objects.filter(role='customer').count()
    total_vendors = User.objects.filter(role='vendor').count()
    pending_vendors = User.objects.filter(role='vendor', is_verified=False).count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    vendors = User.objects.filter(role='vendor').order_by('-created_at')

    context = {
        'total_customers': total_customers,
        'total_vendors': total_vendors,
        'pending_vendors': pending_vendors,
        'total_products': total_products,
        'total_orders': total_orders,
        'vendors': vendors,
    }
    return render(request, 'dashboard/admin/dashboard.html', context)


@admin_required
def vendor_approval(request, vendor_id):
    vendor = get_object_or_404(User, id=vendor_id, role='vendor')

    if request.method == 'POST':
        approved = request.POST.get('approved') == 'true'
        vendor.is_verified = approved
        vendor.save(update_fields=['is_verified'])
        return redirect('admin_dashboard')

    return render(request, 'dashboard/admin/vendor_approval.html', {'vendor': vendor})


@vendor_required
def vendor_dashboard_page(request):
    product_count = Product.objects.filter(vendor=request.user).count()
    total_sales = Order.objects.filter(product__icontains=request.user.shop_name).count()
    context = {
        'product_count': product_count,
        'total_sales': total_sales,
        'vendor_name': request.user.shop_name,
    }
    return render(request, 'dashboard/vendor/dashboard.html', context)


def home_page(request):
    category = Category.objects.all()
    slider = Slider.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()
    context = {
        'brand': brand,
        'category': category,
        'product': product,
        'slider': slider,
    }
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('home_page')
    else:
        form = UserCreateForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='/accounts/login/')
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product)
    return redirect('home_page')


@login_required(login_url='/accounts/login/')
def item_clear(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required(login_url='/accounts/login/')
def item_increment(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product)
    return redirect('cart_detail')


@login_required(login_url='/accounts/login/')
def item_decrement(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.decrement(product=product)
    return redirect('cart_detail')


@login_required(login_url='/accounts/login/')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')


@login_required(login_url='/accounts/login/')
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def Contact_Page(request):
    if request.method == 'POST':
        Contact_us.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
    return render(request, 'contact.html')


@login_required(login_url='/accounts/login/')
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get(settings.CART_SESSION_ID, {})
        for item in cart.values():
            total = item['price'] * item['quantity']
            Order.objects.create(
                user=request.user,
                product=item['name'],
                price=item['price'],
                quantity=item['quantity'],
                image=item.get('image', ''),
                address=address,
                phone=phone,
                pincode=pincode,
                total=total,
            )
        request.session[settings.CART_SESSION_ID] = {}
        request.session.modified = True
        return redirect('home_page')

    return render(request, 'checkout.html')


@login_required(login_url='/accounts/login/')
def Your_Order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order.html', {'order': orders})


def Product_page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()
    return render(request, 'product.html', {'brand': brand, 'category': category, 'product': product})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'detail.html', {'product': product})


def Search(request):
    query = request.GET.get('query', '')
    product = Product.objects.filter(name__icontains=query)
    return render(request, 'search.html', {'product': product})
