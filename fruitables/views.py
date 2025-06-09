from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages

from django.contrib.auth import logout, login, authenticate, update_session_auth_hash

from django.contrib.auth.decorators import login_required

from django.urls import reverse

from .models import CustomUser, Product, SubEmail, Contact, Category, Review, WishList, WishListItem, Cart, CartItem


@login_required
def profile_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'profile.html', {'user': user})

@login_required
def home_view(request):
    email = request.POST.get('email')

    vegetables = Product.objects.filter(category__slug__exact='vegetable')
    best_products = Product.objects.all().order_by('-views')[:6]
    top_products = Product.objects.all().order_by('-views')[:4]

    if email:
        SubEmail.objects.create(email=email)
        messages.success(request, 'You have successfully subscribed to our newsletter!')
        return redirect('home')

    context = {
        'vegetables': vegetables,
        'best_products': best_products,
        'top_products': top_products,
    }

    return render(request, 'index.html', context)

@login_required
def home_view2(request):
    email = request.POST.get('email')

    vegetables = Product.objects.filter(category__slug__exact='vegetable')
    best_products = Product.objects.all().order_by('-views')[:6]
    top_products = Product.objects.all().order_by('-views')[:4]

    if email:
        SubEmail.objects.create(email=email)
        messages.success(request, 'You have successfully subscribed to our newsletter!')
        return redirect('home2')

    context = {
        'vegetables': vegetables,
        'best_products': best_products,
        'top_products': top_products,
    }

    return render(request, 'index-2.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'User logged out successfully')
    return redirect('home')

@login_required
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email:
            Contact.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')

        if email:
            SubEmail.objects.create(email=email)
            messages.success(request, 'You have successfully subscribed to our newsletter!')
            return redirect('contact')

    return render(request, 'contact.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        image = request.FILES.get('image')
        phone_number = request.POST.get('phone_number')
        bio = request.POST.get('bio')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            bio=bio,
            image=image,
            password=password,
        )
        user.save()
        messages.success(request, 'You have successfully registered!')
        login(request, user)
        return redirect('profile', user.pk)

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User logged in successfully')
            return redirect('profile', user.pk)
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')

@login_required
def change_password_view(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Your password has been updated successfully.")
        return redirect('profile', pk=request.user.pk)

    return render(request, 'change_password.html')

@login_required
def shop_view(request):
    if request.method == "POST":
        email = request.POST.get('email')

        if email:
            SubEmail.objects.create(email=email)
            messages.success(request, 'Email added to the list')
            return redirect('shop')

    featured_products = Product.objects.filter(is_featured=True).order_by('-id')
    products = Product.objects.all().order_by('id')

    context = {
        'featured_products': featured_products[:3],
        'products': products[:9],
    }

    return render(request, 'shop.html', context)

@login_required
def about_view(request):
    return render(request, 'about.html')

@login_required
def category_view(request, slug):
    category = get_object_or_404(Category, slug__exact=slug)
    products = Product.objects.filter(category=category).order_by('id')

    if request.method == "POST":
        email = request.POST.get('email')

        if email:
            SubEmail.objects.create(email=email)
            messages.success(request, 'Email added to the list')
            return redirect('category', slug)

    context = {
        'category': category,
        'products': products[:9],
    }

    return render(request, 'category.html', context)

@login_required
def product_detail_view(request, slug):
    name = request.POST.get('name')
    email = request.POST.get('email')
    review = request.POST.get('review', "")

    product = get_object_or_404(Product, slug__exact=slug)
    featured_products = Product.objects.filter(is_featured=True)
    related_products = Product.objects.filter(
        category__slug__iexact=product.category.slug
    ).exclude(pk=product.pk)
    reviews = Review.objects.filter(product=product).order_by('-id')

    if request.method == "POST":
        if name and email:
            Review.objects.create(
                user=request.user,
                product=product,
                name=name,
                email=email,
                review=review,
            )
            messages.success(request, 'Review added')
            return redirect(product.get_absolute_url())

        if email:
            SubEmail.objects.create(email=email)
            messages.success(request, 'Email added to the list')
            return redirect(product.get_absolute_url())
            # return redirect('product_detail', slug)

    context = {
        'product': product,
        'featured_products': featured_products,
        'related_products': related_products,
        'reviews': reviews,
    }

    return render(request, 'shop-detail.html', context)

@login_required
def testimonial_view(request):
    email = request.POST.get('email')
    if request.method == "POST":
        if email:
            SubEmail.objects.create(email=email)
            messages.success(request, 'Email added to the list')
            return redirect('testimonial')
    return render(request, 'testimonial.html')

@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist, wishlist_created = WishList.objects.get_or_create(user=request.user)
    wishlist_item, wishlist_item_created = WishListItem.objects.get_or_create(product=product, wishlist=wishlist)

    if wishlist_created:
        messages.success(request, 'Wishlist created')
    if wishlist_item_created:
        messages.success(request, 'Product added to wishlist')
    if not wishlist_item_created:
        messages.success(request, 'Product already in wishlist')

    return redirect(request.META.get("HTTP_REFERER", reverse("home")))

@login_required
def remove_from_wishlist(request, pk):
    wishlist_item = get_object_or_404(WishListItem, pk=pk)
    wishlist = wishlist_item.wishlist

    if wishlist.user != request.user:
        messages.error(request, "You don't have permission to remove this item.")
        return redirect(request.META.get("HTTP_REFERER", reverse("home")))

    wishlist_item.delete()
    messages.success(request, 'Product removed from your wishlist')

    other_items = WishListItem.objects.filter(wishlist=wishlist).exists()

    if not other_items:
        wishlist.delete()
        messages.info(request, 'Your wishlist is now empty and has been deleted.')

    return redirect(request.META.get("HTTP_REFERER", reverse("home")))

@login_required
def wishlist_view(request):
    email = request.POST.get('email')
    wishlist_items = WishListItem.objects.filter(wishlist__user=request.user)
    if request.method == "POST":
        if email:
            SubEmail.objects.create(email=email)
            messages.success(request, 'Email added to the list')
            return redirect('wishlist')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, cart_created = Cart.objects.get_or_create(user=request.user)
    cart_item, cart_item_created = CartItem.objects.get_or_create(product=product, cart=cart)

    if cart_created:
        messages.success(request, 'Cart created')
    if cart_item_created:
        messages.success(request, 'Product added to cart')
    if not cart_item_created:
        messages.info(request, "Item already in cart")

    return redirect(request.META.get("HTTP_REFERER", reverse("home")))

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart = cart_item.cart

    if cart.user != request.user:
        messages.error(request, "You don't have permission to remove this item.")
        return redirect(request.META.get("HTTP_REFERER", reverse("home")))

    cart_item.delete()
    messages.success(request, 'Product removed from your cart')

    other_items = CartItem.objects.filter(cart=cart).exists()

    if not other_items:
        cart.delete()
        messages.info(request, 'Your cart is now empty and has been deleted.')

    return redirect(request.META.get("HTTP_REFERER", reverse("home")))
