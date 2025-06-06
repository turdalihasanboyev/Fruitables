from django.db import models

from django.utils.text import slugify
from django.urls import reverse

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

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


class Product(BaseModel):
    PRICE_TYPE = (
        ("USD", '$'),
        ("EUR", '€'),
        ("RUB", '₽'),
        ("UZS", "so'm"),
    )

    UNIT_CHOICES = (
        ('Dona', 'dona'),
        ('Kilogramm', 'kg'),
        ('Gramm', 'g'),
        ('Litr', 'l'),
        ('Millilitr', 'ml'),
        ('Metr', 'm'),
        ('Santimetr', 'sm'),
        ('Kvadrat metr', 'm2'),
        ('Kub metr', 'm3'),
        ('Qop', 'qop'),
        ('Blok', 'blok'),
        ('Dasta', 'dasta'),
        ('Paket', 'paket'),
        ('Karta', 'karta'),
    )

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE, default='USD')
    unit_type = models.CharField(max_length=25, choices=UNIT_CHOICES, default='Dona')
    percentage = models.PositiveIntegerField(default=0)
    weight = models.CharField(max_length=100, null=True, blank=True)
    country_of_orign = models.CharField(max_length=100, null=True, blank=True)
    quality = models.CharField(max_length=100, null=True, blank=True)
    check_status = models.CharField(max_length=100, null=True, blank=True)
    min_weight = models.CharField(max_length=100, null=True, blank=True)

    @property
    def discount(self):
        if self.percentage:
            discount_amount = int((self.price * self.percentage) / 100)
            return int(self.price - discount_amount)
        return int(self.price)

    @property
    def average_rating(self):
        average = self.review_product.aggregate(avg_rate=Avg('rate'))['avg_rate']
        return round(average, 2) if average else 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'ID: {self.id} - Name: {self.name} - Category: {self.category} - Price: {self.price} - Discount: {self.discount} - Price Type: {self.price_type} - Unit Type {self.unit_type} - Rating: {self.average_rating}'


class Review(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='review_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_product')
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    rate = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'ID: {self.id} - User: {self.user} - Product: {self.product} - Rate: {self.rate}'
