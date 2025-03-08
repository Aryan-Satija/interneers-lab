from django.urls import path
from . import views

urlpatterns = [
    path('getall', views.getProductList),
    path('add', views.addProduct),
    path('addBrand', views.addBrand),
    path('addCategory', views.addCategory),
    path('update', views.updateProduct),
    path('delete', views.deleteProduct),
    path('get/<int:productId>', views.getProduct)
]