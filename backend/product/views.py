from django.shortcuts import render
from .models import Product, Category, Brand
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def addBrand(request):
    name = request.data.get('name')
    if not name:
        return Response({"error": "Brand name is required"})
    
    if Brand.objects.filter(name=name).exists():
        return Response({"error": "Brand already exists"})
    
    brand = Brand.objects.create(name=name)

    return Response({"message": "Brand created successfully", "id": brand.id, "name": brand.name})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def addCategory(request):
    name = request.data.get('name')
    if not name:
        return Response({"error": "Category name is required"})
    
    if Category.objects.filter(name=name).exists():
        return Response({"error": "Category already exists"})
    
    category = Category.objects.create(name=name)

    return Response({"message": "Category created successfully", "id": category.id, "name": category.name})

