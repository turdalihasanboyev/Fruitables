from django.contrib import admin

from .models import (
    SubEmail,
    CustomUser
)


admin.site.register(CustomUser)
admin.site.register(SubEmail)
