from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Product
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .forms import SignUpForm, UserUpdateForm, PasswordUpdateForm

## Vista para registrar un proveedor
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

# Vista para editar información de usuario
@login_required
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordUpdateForm(request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password = password_form.cleaned_data.get('password')
            if password:
                request.user.set_password(password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Para mantener la sesión después de cambiar la contraseña
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordUpdateForm()
    return render(request, 'registration/user_update.html', {'user_form': user_form, 'password_form': password_form})

# Vista de perfil de usuario
@login_required
def profile(request):
    return render(request, 'registration/profile.html')

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