from django.contrib import admin

from .models import (
    SubEmail,
    CustomUser,
    Testimonial,
    Contact,
    Category,
    Product,
    Review,
    WishList,
    WishListItem,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


admin.site.register(CustomUser)
admin.site.register(SubEmail)
admin.site.register(Testimonial)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(WishList)
admin.site.register(WishListItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
