from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Category, Product, Order, Brand, Slider, Contact_us, UserCreateForm

from cart.cart import Cart

from .serializers import CategorySerializer, ProductSerializer, BrandSerializer, OrderSerializer





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
