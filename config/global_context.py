from fruitables.models import Category, Product, Testimonial, WishListItem, CartItem

def global_context(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    testimonials = Testimonial.objects.all()
    wishlist_items_count = WishListItem.objects.filter(wishlist__user=request.user).count()
    cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
    context = {
        'categories': categories,
        'products': products,
        'testimonials': testimonials,
        'wishlist_items_count': wishlist_items_count,
        'cart_items_count': cart_items_count,
    }
    return context