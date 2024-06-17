from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'proveedores'

urlpatterns = [
    # URL para la lista de productos
    path('', views.ProductListView.as_view(), name='product_list'),
    # URL para el detalle de un producto
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    # URL para crear un nuevo producto
    path('new/', views.product_new, name='product_new'),
    # URL para editar un producto
    path('<int:pk>/edit/', views.product_update, name='product_update'),
    # URL para eliminar un producto
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    # URL para el login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # URL para el registro
    path('signup/', views.signup, name='signup'),
    # URL para el perfil de usuario
    path('profile/', views.profile, name='profile'),
    # URL para editar el perfil de usuario
    path('profile/edit/', views.user_update, name='user_update'),
    # URL para el logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]