from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth import logout, login, authenticate, update_session_auth_hash

from django.db.models import Avg

from .models import CustomUser, Product, SubEmail, Contact, Category, Review


@login_required
def profile_view(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    return render(request, 'profile.html', {'user': user})

@login_required
def home_view(request):
    email = request.POST.get('email')

    vegetables = Product.objects.filter(category__name__icontains='Vegetable')
    best_products = Product.objects.all().order_by('-views')[:6]
    top_products = Product.objects.all().order_by('-views')[:4]

    if email:
        SubEmail.objects.create(email=email)
        messages.success(request, 'You have successfully subscribed to our newsletter!')

    context = {
        'vegetables': vegetables,
        'best_products': best_products,
        'top_products': top_products,
    }

    return render(request, 'index.html', context)

@login_required
def home_view2(request):
    email = request.POST.get('email')

    vegetables = Product.objects.filter(category__name__icontains='Vegetable')
    best_products = Product.objects.all().order_by('-views')[:6]
    top_products = Product.objects.all().order_by('-views')[:4]

    if email:
        SubEmail.objects.create(email=email)
        messages.success(request, 'You have successfully subscribed to our newsletter!')

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
        return redirect('profile', user.id)

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User logged in successfully')
            return redirect('profile', user.id)
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
        return redirect('profile', pk=request.user.id)

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
    )
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
