from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import CustomerProfile
from orders.models import Order

class CustomerLoginView(LoginView):
    template_name = 'customers/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('customers:dashboard')

class CustomerRegistrationView(CreateView):
    template_name = 'customers/register.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('customers:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, _('Your account has been created successfully!'))
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Register')
        return context

@login_required
def dashboard(request):
    # Get recent orders
    recent_orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    # Get saved addresses
    addresses = request.user.addresses.all()
    
    return render(request, 'customers/dashboard.html', {
        'recent_orders': recent_orders,
        'addresses': addresses,
    })

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated.'))
            return redirect('customers:profile')
    else:
        form = CustomerProfileForm(instance=profile)
    
    return render(request, 'customers/profile.html', {
        'form': form,
    })

@login_required
def addresses(request):
    addresses = request.user.addresses.all()
    return render(request, 'customers/addresses.html', {
        'addresses': addresses,
    })

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'customers/orders.html', {
        'orders': orders,
    })

def logout_view(request):
    logout(request)
    messages.success(request, _('You have been logged out successfully.'))
    return redirect('catalog:home')
