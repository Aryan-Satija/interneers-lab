from django.urls import path
from . import views

urlpatterns = [
    path('getall', views.getProductList),
    path('add', views.addProduct)
]