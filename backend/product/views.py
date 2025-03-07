from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

products = []
categories = []
brands = []

@api_view(['GET'])
def getProductList(request):
    return Response(products)

@api_view(['POST'])
def addProduct(request):
    category_id = request.data.get('category')
    brand_id = request.data.get('brand')
    
    if category_id > len(categories):
        return Response({"error": "Category does not exist"}, status=400)

    if brand_id > len(brands):
        return Response({"error": "Brand does not exist"}, status=400)

    product = {
        "id": len(products) + 1,
        "name": request.data.get("name"),
        "description": request.data.get("description", ""),
        "price": request.data.get("price", 0),
        "quantity": request.data.get("quantity", 0),
        "brand": brand_id,
        "category": category_id
    }
    products.append(product)
    return Response(product, status=201)

@api_view(['POST'])
def addBrand(request):
    name = request.data.get('name')

    if not name:
        return Response({"error": "Brand name is required"}, status=400)

    if any(brand['name'] == name for brand in brands):
        return Response({"error": "Brand already exists"}, status=400)

    brand = {"id": len(brands) + 1, "name": name}
    brands.append(brand)
    return Response({"message": "Brand created successfully", "brand": brand}, status=201)

@api_view(['POST'])
def addCategory(request):
    name = request.data.get('name')

    if not name:
        return Response({"error": "Category name is required"}, status=400)

    if any(category['name'] == name for category in categories):
        return Response({"error": "Category already exists"}, status=400)

    category = {"id": len(categories) + 1, "name": name}
    categories.append(category)
    return Response({"message": "Category created successfully", "category": category}, status=201)