from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Product, Category, ProductVariant

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug:
            # Get the category using translated slug
            category = Category.objects.translated(slug=category_slug).first()
            if category:
                queryset = queryset.filter(category=category)
        
        return queryset.prefetch_related(
            'variants',
            'images',
            'category'
        ).filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            # Get the product using translated slug
            product = Product.objects.translated(slug=slug).prefetch_related(
                'variants',
                'images',
                'category'
            ).first()
            if product:
                return product
        
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.filter(is_active=True)[:4]
            )
        )

def home(request):
    # Get featured products
    featured_products = Product.objects.filter(
        is_active=True,
        featured=True
    ).prefetch_related('variants', 'images')[:8]
    
    # Get latest products
    new_arrivals = Product.objects.filter(
        is_active=True
    ).order_by('-created_at')[:8]
    
    # Get active categories with their translations
    # Using django-parler's translated() manager to order by translated field
    categories = Category.objects.translated().filter(
        is_active=True
    ).order_by(
        'translations__name'
    )[:6]
    
    # Get the IDs of our selected categories
    category_ids = [cat.id for cat in categories]
    
    # Prefetch products for these specific categories
    categories = Category.objects.translated().filter(
        id__in=category_ids
    ).prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(
                is_active=True
            ).order_by('?')
        )
    )
    
    return render(request, 'catalog/home.html', {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
    })
