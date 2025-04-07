from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list_create, name='product-list'),
    path('product/<product_id>/', views.product_detail, name='product-detail'),
    path('brand/', views.add_brand, name='brand-add'),
    path('category/', views.add_category, name='category-add'),
]