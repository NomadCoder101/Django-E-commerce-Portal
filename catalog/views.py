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
            queryset = queryset.filter(category__slug=category_slug)
        
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

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'variants',
            'images',
            'category'
        )

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
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).prefetch_related('variants', 'images')[:8]
    
    new_arrivals = Product.objects.filter(
        is_active=True
    ).order_by('-created_at')[:8]
    
    categories = Category.objects.prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(is_active=True)[:4]
        )
    )[:6]
    
    return render(request, 'catalog/home.html', {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
    })
