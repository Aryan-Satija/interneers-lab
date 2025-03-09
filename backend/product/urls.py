from django.urls import path
from . import views

urlpatterns = [
    path('getProductList/', views.get_product_list),
    path('addProduct', views.add_product),
    path('addBrand', views.add_brand),
    path('addCategory', views.add_category),
    path('updateProduct', views.update_product),
    path('deleteProduct', views.delete_product),
    path('getProduct/<int:product_id>', views.get_product)
]