from fruitables.models import Category, Product, Testimonial, WishListItem

def global_context(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    testimonials = Testimonial.objects.all()
    wishlist_items_count = WishListItem.objects.filter(wishlist__user=request.user).count()
    context = {
        'categories': categories,
        'products': products,
        'testimonials': testimonials,
        'wishlist_items_count': wishlist_items_count,
    }
    return context