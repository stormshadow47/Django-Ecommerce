from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from Products.models import Product
from Users.models import Review


def home(request):
    """Home page with featured products"""
    products = Product.objects.all()[:8]
    return render(request, 'products.html', {'products': products})


def products_list(request):
    """Products listing page"""
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def product_detail(request, product_id):
    """Product detail page"""
    try:
        product = Product.objects.get(id=product_id)
        reviews = Review.objects.filter(product=product)
        return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


@login_required
def cart_page(request):
    """Cart page"""
    from cart.models import Cart
    try:
        cart = Cart.objects.get(user=request.user)
        # Calculate total price
        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        cart.total_price = total_price
        return render(request, 'cart.html', {'cart': cart})
    except Cart.DoesNotExist:
        return render(request, 'cart.html', {'cart': None})


def login_page(request):
    """Login page"""
    return render(request, 'login.html')


def register_page(request):
    """Register page"""
    return render(request, 'register.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    if request.headers.get('HX-Request'):
        from django.http import HttpResponse
        return HttpResponse(status=200, headers={'HX-Redirect': '/'})
    return redirect('/')


def search_products(request):
    """Search products API for htmx"""
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'partials/product_list.html', {'products': products})


def cart_count_partial(request):
    """Return cart count for htmx updates"""
    from cart.models import Cart
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.items.count()
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        cart_count = 0
    return render(request, 'partials/cart_count.html', {'cart_count': cart_count})


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    from orders.models import Order, OrderItem
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        return render(request, 'order_confirmation.html', {'order': order, 'order_items': order_items})
    except Order.DoesNotExist:
        return redirect('/products/')
