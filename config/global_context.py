from fruitables.models import Category, Product, Testimonial

def global_context(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    testimonials = Testimonial.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'testimonials': testimonials,
    }
    return context