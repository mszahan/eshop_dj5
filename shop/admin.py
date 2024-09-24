from django.contrib import admin
from .models import Product, Category, Gallery, Variation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class GalleryInline(admin.StackedInline):
    model = Gallery
    extra = 0

class VariationInline(admin.StackedInline):
    model = Variation
    prepopulated_fields = {'slug': ('name',)}
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryInline, VariationInline ]