from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list_create),
    path('product/<int:product_id>/', views.product_detail),
    path('brand/', views.add_brand),
    path('category/', views.add_category),
]