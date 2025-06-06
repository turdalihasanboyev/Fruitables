from django.contrib import admin

from .models import (
    SubEmail,
    CustomUser,
    Testimonial,
    Contact,
    Category,
    Product,
    Review,
)


admin.site.register(CustomUser)
admin.site.register(SubEmail)
admin.site.register(Testimonial)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
