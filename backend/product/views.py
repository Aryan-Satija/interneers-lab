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

@api_view(['POST'])
def addProduct(request):
    category_id = request.data.get('category')
    brand_id = request.data.get('brand')
    
    if not Category.objects.filter(id=category_id).exists():
        return Response({"error": "Category does not exist"})

    if not Brand.objects.filter(id=brand_id).exists():
        return Response({"error": "Brand does not exist"})
    
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)