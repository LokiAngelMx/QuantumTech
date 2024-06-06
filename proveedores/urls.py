from django.urls import path
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
]