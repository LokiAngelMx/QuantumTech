from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Product
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

# Vista para registrar un proveedor
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Vista de lista de productos
class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'proveedores/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user).order_by('-id')

# Vista de detalle de producto
class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    template_name = 'proveedores/product_detail.html'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

# Vista para crear un producto
@login_required
def product_new(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        if name and price and description:
            Product.objects.create(user=request.user, name=name, price=price, description=description)
            return redirect('proveedores:product_list')
    return render(request, 'proveedores/product_edit.html', {'product': None})

# Vista para actualizar un producto
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.price = request.POST.get('price', product.price)
        product.description = request.POST.get('description', product.description)
        product.save()
        return HttpResponseRedirect(reverse('proveedores:product_detail', args=[product.pk]))
    return render(request, 'proveedores/product_edit.html', {'product': product})

# Vista para eliminar un producto
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('proveedores:product_list')