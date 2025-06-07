from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth import logout

from django.db.models import Avg

from .models import CustomUser, Product, SubEmail


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
