from django.urls import path

from .views import (
    profile_view,
    home_view,
    home_view2,
    logout_view,
)


urlpatterns = [
    path('', home_view, name='home'),
    path('home2/', home_view2, name='home2'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
]
