from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dataclasses import dataclass
from typing import Optional, List
from .exceptions import ProductNotFound, InvalidProductId, ProductValidationError, CategoryValidationError, BrandValidationError
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

        try:
            products = product_service.get_paginated_products(page, page_size, get_product_request, sort_by)
            return Response({
                'page': page,
                'page_size': page_size,
                'products': products
            }) 
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        

    elif request.method == 'POST':
        try:    
            data = product_service.create_product(request.data)
            return Response(data, status=201)
        except (ValueError, ProductValidationError) as e:
            return Response({"error": str(e)}, 400)
        except Exception as e:
            return Response({"error": "Something went wrong"}, 500)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, product_id):
    if request.method == 'GET':
        try:
            product = product_service.get_product_by_id(product_id)
        except ProductNotFound as e:
            return Response({"error": str(e)}, status=404)
        except InvalidProductId as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": "Something went wrong"}, status=500)

        return Response({"product": product}, status=200)
        
    elif request.method == 'PUT':
        try:
            product_service.update_product(product_id, request.data)
        except (ValueError, InvalidProductId, ProductValidationError) as e:
            return Response({"error": str(e)}, status=400)
        except ProductNotFound as e:
            return Response({"error": str(e)}, status=404)
        
        return Response({"message": "Product updated successfully"}, status=200)
    
    elif request.method == 'DELETE':
        try:
            product_service.delete_product(product_id)
        except InvalidProductId as e:
            return Response({"error": str(e)}, status=400)
        except ProductNotFound as e:
            return Response({"error": str(e)}, status=404)
        return Response({"message": "Product Deleted Successfully"}, status=204) 


@api_view(['GET', 'POST'])
def add_brand(request):
    if request.method == 'GET':
        try:
            data = brand_service.get_brands()
            return Response({"brands": data}, status=200)
        except Exception as e:
            return Response({"error": "Something went wrong"}, status=500)
    else:        
        try:
            data = brand_service.create_brand(request.data)
            return Response({data}, status=201)
        except BrandValidationError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": "Something went wrong"}, status=500)   

@api_view(['GET', 'POST'])
def add_category(request):
    if request.method == "GET":
        try:
            data = category_service.get_categories()
            return Response({"categories": data}, status=200)
        except Exception as e:
            return Response({"error": "Something went wrong"}, status=500)
    else:            
        try:
            data = category_service.create_category(request.data)
            return Response(data, status=201)
        except CategoryValidationError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": "Something went wrong"}, status=500)