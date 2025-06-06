from django.db import models

from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SubEmail(BaseModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.id} - {self.email}'


class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.id} - {self.first_name} {self.last_name}'
        if self.email:
            return f'{self.id} - {self.email}'
        if self.phone_number:
            return f'{self.id} - {self.phone_number}'
        return f'{self.id} - {self.username}'
