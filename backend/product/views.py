from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services.product_service import ProductService
from .services.brand_service import BrandService
from .services.category_service import CategoryService


@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        try:
            page_size = int(request.GET.get('page_size', 10))
            page = int(request.GET.get('page', 1))
        except ValueError:
            return Response({"error": "Invalid page or page_size value"}, status=400)

        products = ProductService.get_paginated_products(page, page_size)
        
        return Response({
            'page': page,
            'page_size': page_size,
            'products': products
        }) 

    elif request.method == 'POST':
        data, error = ProductService.create_product(request.data)
        
        if error:
            return Response(error, status=400)
        
        return Response(data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, product_id):
    if request.method == 'GET':
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return Response({"error": "Product does not exist"}, status=404)
        
        return Response(product)
        
    elif request.method == 'PUT':
        data, error = ProductService.update_product(product_id, request.data)
        
        if error:
            return Response(error, status=400)
        
        return Response(data, status=201)
    
    elif request.method == 'DELETE':
        ProductService.delete_product(product_id)
        return Response({"message": "Product Deleted Successfully"}, status=204)


@api_view(['POST'])
def add_brand(request):
    data, error = BrandService.create_brand(request.data)
    
    if error:
        return Response(error, status=400)
    
    return Response(data, status=201)


@api_view(['POST'])
def add_category(request):
    data, error = CategoryService.create_category(request.data)
    
    if error:
        return Response(error, status=400)
    
    return Response(data, status=201)
