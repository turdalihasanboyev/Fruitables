from django.db import models

from django.utils.text import slugify

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


class Contact(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.name} - {self.email}'


class Testimonial(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonial_images', null=True, blank=True)
    job = models.CharField(max_length=100)
    testimonial = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.name} - {self.job}'


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} - {self.name}'
