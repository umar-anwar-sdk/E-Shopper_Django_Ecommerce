from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import generics, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

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





@api_view(['GET'])
def product_api(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail_api(request, id):
    product = Product.objects.get(id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def category_api(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def brand_api(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)




from django.shortcuts import get_object_or_404

@api_view(['POST'])
def add_to_cart(request):

    product_id = request.data.get('product_id')

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            "name": product.name,
            "price": product.price,
            "quantity": 1
        }

    request.session['cart'] = cart
    request.session.modified = True

    return Response({"message": "Product added to cart", "cart": cart})
@api_view(['GET'])
def view_cart(request):
    cart = request.session.get('cart', {})
    return Response(cart)
@api_view(['POST'])
def remove_from_cart(request):
    product_id = request.data['product_id']

    cart = request.session.get('cart', {})

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return Response({"message": "Removed"})

@api_view(['POST'])
def place_order(request):

    from django.contrib.auth.models import User

    user = User.objects.first()

    cart = request.session.get('cart', {})

    for item in cart.values():

        Order.objects.create(
            user=user,
            product=item['name'],
            price=item['price'],
            quantity=item['quantity'],
        )

    request.session['cart'] = {}

    return Response({"message": "Order placed"})
@api_view(['GET'])
def my_orders(request):
    from django.contrib.auth.models import User

    user = User.objects.first()

    orders = Order.objects.filter(user=user)

    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)
@api_view(['PATCH'])  # or ['PUT']
def update_product(request, id):
    product = Product.objects.get(id=id)
    serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)
@api_view(['DELETE'])
def delete_product(request, id):

    product = Product.objects.get(id=id)
    product.delete()

    return Response({"message": "Product deleted"})
@api_view(['POST'])
def create_product(request):

    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)

@api_view(['GET'])
def search_product(request):

    keyword = request.GET.get('keyword', '')

    products = Product.objects.filter(
        Q(name__icontains=keyword) |
        Q(brand__name__icontains=keyword)
    )

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
def cart_total(request):

    cart = request.session.get('cart', {})

    total = 0

    for item in cart.values():

        total += item['price'] * item['quantity']

    return Response({"total": total})

@api_view(['POST'])
def increment_cart(request):

    product_id = request.data.get('product_id')

    if not product_id:
        return Response({"error": "product_id is required"}, status=400)

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
        message = "Quantity increased"
    else:
        return Response({"error": "Product not in cart"}, status=404)

    request.session['cart'] = cart
    request.session.modified = True

    return Response({"message": message, "cart": cart})
@api_view(['POST'])
def decrement_cart(request):

    product_id = request.data.get('product_id')

    if not product_id:
        return Response({"error": "product_id is required"}, status=400)

    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id not in cart:
        return Response({"error": "Product not in cart"}, status=404)

    cart[product_id]['quantity'] -= 1

    if cart[product_id]['quantity'] <= 0:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return Response({
        "message": "Quantity decreased",
        "cart": cart
    })


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """List products for everyone and allow admins/vendors to create products."""
    queryset = Product.objects.select_related('brand', 'Category', 'vendor').all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrVendor()]

    def perform_create(self, serializer):
        if self.request.user.is_vendor():
            serializer.save(vendor=self.request.user)
            return

        if self.request.user.is_admin():
            vendor_id = self.request.data.get('vendor') or self.request.data.get('vendor_id')
            if vendor_id:
                try:
                    vendor = User.objects.get(id=vendor_id, role='vendor')
                    serializer.save(vendor=vendor)
                    return
                except User.DoesNotExist:
                    raise serializers.ValidationError({'vendor': 'Vendor not found.'})
            serializer.save(vendor=self.request.user)
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
    permission_classes = [IsAuthenticated(), IsVendorUserRole]

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user).select_related('brand', 'Category')


class AdminProductListAPIView(generics.ListAPIView):
    """Admin view of all products."""
    queryset = Product.objects.all().select_related('brand', 'Category', 'vendor')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated(), IsAdminUserRole]


class VendorBrandUpdateAPIView(generics.UpdateAPIView):
    """Allow a vendor to update branding and banner assets."""
    serializer_class = None
    permission_classes = [IsAuthenticated(), IsVendorUserRole]

    def get_serializer_class(self):
        from authentication.serializers import UpdateProfileSerializer
        return UpdateProfileSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class VendorDashboardAPIView(generics.RetrieveAPIView):
    """Vendor dashboard with product counts and ownership stats."""
    permission_classes = [IsAuthenticated(), IsVendorUserRole]

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):

    user = request.user

    orders = Order.objects.filter(user=user)

    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)

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
    return render(request, "index.html", context)


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
    context = {
        'form': form,
    }
    return render(request, "registration/signup.html", context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home_page")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


# Contact

def Contact_Page(request):
    if request.method == "POST":
        contact = Contact_us(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        contact.save()
    return render(request, 'contact.html')


def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a * b
            order = Order(
                user=user,
                product=cart[i]['name'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                phone=phone,
                pincode=pincode,
                total=total,
            )
            order.save()
        request.session['cart'] = {}
        return redirect("home_page")

    return render(request, 'checkout.html')


def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)

    order = Order.objects.filter(user=user)
    context = {
        'order': order,
    }
    return render(request, 'order.html', context)


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
    context = {
        'brand': brand,
        'category': category,
        'product': product,
    }
    return render(request, 'product.html', context)

def product_detail(request, id):
    product = Product.objects.get(id=id)

    context = {
        'product': product,
    }
    return render(request, 'detail.html', context)


def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains=query)
    context = {
        'product': product,
    }
    return render(request, 'search.html', context)
