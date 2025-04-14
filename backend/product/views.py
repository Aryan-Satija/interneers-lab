from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dataclasses import dataclass
from typing import Optional, List
from .services.product_service import ProductService
from .services.brand_service import BrandService
from .services.category_service import CategoryService
product_service = ProductService()
brand_service = BrandService()
category_service = CategoryService()


@dataclass
class GetProductRequest:
    name: Optional[str] = None
    min_price: Optional[str] = None
    max_price: Optional[str] = None
    brand: Optional[List[str]] = None
    category: Optional[List[str]] = None

@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        try:
            page_size = int(request.GET.get('page_size', 10))
            page = int(request.GET.get('page', 1))
            sort_by = request.GET.get('sort_by', '-created_at')
            get_product_request = GetProductRequest(                
                name = request.GET.get('name', None),
                min_price = request.GET.get('min_price', None),
                max_price = request.GET.get('max_price', None),
                brand = request.GET.get('brand', None).split(',') if request.GET.get('brand', None) else None,
                category = request.GET.get('category', None).split(',') if request.GET.get('category', None) else None
            )
        except ValueError:
            return Response({"error": "Invalid page or page_size value"}, status=400)

        products = product_service.get_paginated_products(page, page_size, get_product_request, sort_by)
        
        return Response({
            'page': page,
            'page_size': page_size,
            'products': products
        }) 

    elif request.method == 'POST':
        data, error = product_service.create_product(request.data)
        
        if error:
            return Response(error, status=400)
        
        return Response(data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, product_id):
    if request.method == 'GET':
        product = product_service.get_product_by_id(product_id)
         
        if not product:
            return Response({"error": "Product does not exist"}, status=404)
        
        return Response({"product": product}, status=200)
        
    elif request.method == 'PUT':
        data, error = product_service.update_product(product_id, request.data)
        
        if error:
            return Response(error, status=400)
        
        return Response(data, status=201)
    
    elif request.method == 'DELETE':
        response, is_error = product_service.delete_product(product_id)
        return Response(response, status=204) if not is_error else Response(response, 404)


@api_view(['POST'])
def add_brand(request):
    data, error = brand_service.create_brand(request.data)
    
    if error:
        return Response(error, status=400)
    
    return Response(data, status=201)


@api_view(['POST'])
def add_category(request):
    data, error = category_service.create_category(request.data)
    
    if error:
        return Response(error, status=400)
    
    return Response(data, status=201)
