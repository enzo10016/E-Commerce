from django.shortcuts import render, redirect
from django.conf import settings
from .models import Product
from .forms import ProductForm
import os

# Mock or Real OpenAI Integration
def generate_tags(name, description):
    # Retrieve the key from settings
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    
    # Simple logic fallback if key is missing or for this activity
    base_tags = [name.lower(), "ecommerce", "premium"]
    words = description.lower().split()
    extra_tags = [w for w in words if len(w) > 4][:3]
    return list(set(base_tags + extra_tags))

def product_list(request):
    products = Product.objects.all()
    # Simple recommendation: suggest products from the same category as the last added one
    # If no products, recommendations will be empty
    last_product = Product.objects.all().order_by('-_id').first()
    recommendations = []
    if last_product:
        recommendations = Product.objects.filter(category=last_product.category).exclude(_id=last_product._id)[:3]
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'recommendations': recommendations
    })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            # Challenge: Auto-suggest tags using "AI" logic
            product.tags = generate_tags(product.name, product.description)
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})
