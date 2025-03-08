from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

products = {}
categories = {}
brands = {}
isCategory = {}
isBrand = {}
index = 1
brandIndex = 1
categoryIndex = 1

@api_view(['GET'])
def getProductList(request):
    page = int(request.GET.get('page', 1))
    pageSize = int(request.GET.get('page_size', 10))
    
    productList = list(products.values())
    
    totalProducts = len(products)
    
    start = (page-1)*pageSize
    end = start + pageSize
    
    return Response({
        "page": page,
        "pageSize": pageSize,
        "products": productList[start:end], 
    })

@api_view(['POST'])
def addProduct(request):
    global index
    category_id = request.data.get('category')
    brand_id = request.data.get('brand')
    
    if category_id not in categories:
        return Response({"error": "Category does not exist"}, status=400)

    if brand_id not in brands:
        return Response({"error": "Brand does not exist"}, status=400)

    product = {
        "name": request.data.get("name"),
        "description": request.data.get("description", ""),
        "price": request.data.get("price", 0),
        "quantity": request.data.get("quantity", 0),
        "brand": brand_id,
        "category": category_id
    }
    
    products[index] = product
    
    index += 1
    
    return Response(product, status=201)

@api_view(['POST'])
def updateProduct(request):
    category_id = request.data.get('category')
    brand_id = request.data.get('brand')
    product_id = request.data.get('product')
    
    if product_id not in products:
        return Response({"error": "Product does not exist"}, status=400)

    if category_id not in categories:
        return Response({"error": "Category does not exist"}, status=400)

    if brand_id not in brands:
        return Response({"error": "Category does not exist"}, status=400)
    
    product = {
        "name": request.data.get("name"),
        "description": request.data.get("description", ""),
        "price": request.data.get("price", 0),
        "quantity": request.data.get("quantity", 0),
        "brand": brand_id,
        "category": category_id
    }
    
    products[product_id] = product
    
    return Response(product, status=201)

@api_view(['POST'])
def deleteProduct(request):
    product_id = request.data.get('product')
    
    if product_id not in products:
        return Response({"error": "Product does not exist"}, status=400)
    
    del products[product_id]
    
    return Response({"success": True}, status=201)

@api_view(['POST'])
def addBrand(request):
    global brandIndex
    name = request.data.get('name')

    if not name:
        return Response({"error": "Brand name is required"}, status=400)

    if name in isBrand:
        return Response({"error": "Brand already exists"}, status=400)

    brand = {"id": brandIndex, "name": name}
    brands[brandIndex] = brand
    brandIndex += 1
    isBrand[name] = True
    return Response({"message": "Brand created successfully", "brand": brand}, status=201)

@api_view(['GET'])
def getProduct(request, productId):
    if productId not in products:
        return Response({
            "error": "Product does not exist",
        }, 400)
    return Response(products[productId])

@api_view(['POST'])
def addCategory(request):
    global categoryIndex
    name = request.data.get('name')

    if not name:
        return Response({"error": "Category name is required"}, status=400)

    if name in isCategory:
        return Response({"error": "Category already exists"}, status=400)

    category = {"id": categoryIndex, "name": name}
    categories[categoryIndex] = category
    categoryIndex += 1
    isCategory[name] = True
    return Response({"message": "Category created successfully", "category": category}, status=201)