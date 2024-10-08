from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Variation



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category, 
        'categories': categories, 
        'products': products})



def product_detail(request, id, slug, variation_slug=None):
    variation = None
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    if variation_slug:
        variation = get_object_or_404(Variation, product=product, slug=variation_slug)
    return render(request, 'shop/product/detail.html', {'product': product, 'variation': variation})