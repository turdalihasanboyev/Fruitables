from django.contrib import admin

from .models import (
    SubEmail,
    CustomUser,
    Testimonial,
    Contact,
    Category,
)


admin.site.register(CustomUser)
admin.site.register(SubEmail)
admin.site.register(Testimonial)
admin.site.register(Contact)
admin.site.register(Category)
