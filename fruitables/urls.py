from django.urls import path

from .views import (
    profile_view,
    home_view,
    home_view2,
    logout_view,
    contact_view,
    register_view,
    login_view,
    change_password_view,
    shop_view,
    about_view,
    category_view,
)


urlpatterns = [
    path('', home_view, name='home'),
    path('home2/', home_view2, name='home2'),
    path('contact/', contact_view, name='contact'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('change-password/', change_password_view, name='change_password'),
    path('shop/', shop_view, name='shop'),
    path('about/', about_view, name='about'),
    path('category/<slug:slug>/', category_view, name='category'),
]
