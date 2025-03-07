from django.shortcuts import render
from .models import Product, Category, Brand
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer

@api_view(['GET'])
def getProductList(request):
    products = Product.objects.all()   
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
