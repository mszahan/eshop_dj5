from django.db import models
from django.db.models import Sum
from django.urls import reverse
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']), ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    # image = models.ImageField(upload_to='porducts/%Y/%m', blank=True)
    description = HTMLField(blank=True)
    short_description = models.TextField(blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
    def total_variation_stock(self):
        return self.variations.aggregate(total=Sum('stock'))['total'] or 0



class Variation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True)
    stock = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_variation', args=[self.product.id, self.product.slug, self.slug])

class Gallery(models.Model):
    product = models.ForeignKey(Product, related_name='galleries', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='porducts/%Y/%m', blank=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        verbose_name = 'gallery'
        verbose_name_plural = 'galleries'
