from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductsSerializer, CategorySerializer, BrandSerializer
from .models import Products, Category, Brand

@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        try:
            page_size = int(request.GET.get('page_size', 10))
            page = int(request.GET.get('page', 1))
        except ValueError:
            return Response({"error": "Invalid page or page_size value"}, status=400)

        start = (page - 1) * page_size
        end = start + page_size

        products = Products.objects.all()[start:end]
        serializer = ProductsSerializer(products, many=True)

        return Response({
            'page': page,
            'page_size': page_size,
            'products': serializer.data
        }) 

    elif request.method == 'POST':
        serializer = ProductsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, product_id):
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=404)
    
    if request.method == 'GET':
        serializer = ProductsSerializer(product)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response({"message": "Product Deleted Successfully"}, status=204)


@api_view(['POST'])
def add_brand(request):
    serializer = BrandSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Brand Created Successfully", "brand": serializer.data}, status=201)
    
    return Response(serializer.errors, status=400) 


@api_view(['POST'])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Category Created Successfully", "category": serializer.data}, status=201)
    
    return Response(serializer.errors, status=400)
