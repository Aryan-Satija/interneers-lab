from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

products = {}
categories = {}
brands = {}
isCategory = {}
isBrand = {}
index = 1
brand_index = 1
category_index = 1

@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        product_list = list(products.values())
        start = (page - 1) * page_size
        end = start + page_size

        return Response({
            "page": page,
            "pageSize": page_size,
            "products": product_list[start:end],
        })

    elif request.method == 'POST':
        global index
        category_id = request.data.get('category')
        brand_id = request.data.get('brand')

        if category_id not in categories:
            return Response({"error": "Category does not exist"}, status=400)

        if brand_id not in brands:
            return Response({"error": "Brand does not exist"}, status=400)

        product = {
            "id": index,
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


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, product_id):
    if product_id not in products:
        return Response({"error": "Product does not exist"}, status=400)

    if request.method == 'GET':
        return Response(products[product_id])

    elif request.method == 'PUT':
        category_id = request.data.get('category')
        brand_id = request.data.get('brand')

        if category_id not in categories:
            return Response({"error": "Category does not exist"}, status=400)

        if brand_id not in brands:
            return Response({"error": "Brand does not exist"}, status=400)

        products[product_id] = {
            "name": request.data.get("name"),
            "description": request.data.get("description", ""),
            "price": request.data.get("price", 0),
            "quantity": request.data.get("quantity", 0),
            "brand": brand_id,
            "category": category_id
        }

        return Response(products[product_id], status=200)

    elif request.method == 'DELETE':
        del products[product_id]
        return Response({"success": True}, status=204)
    
    
@api_view(['POST'])
def add_brand(request):
    global brand_index
    name = request.data.get('name')

    if not name:
        return Response({"error": "Brand name is required"}, status=400)

    if name in isBrand:
        return Response({"error": "Brand already exists"}, status=400)

    brand = {"id": brand_index, "name": name}
    brands[brand_index] = brand
    brand_index += 1
    isBrand[name] = True
    return Response({"message": "Brand created successfully", "brand": brand}, status=201)

@api_view(['POST'])
def add_category(request):
    global category_index
    name = request.data.get('name')

    if not name:
        return Response({"error": "Category name is required"}, status=400)

    if name in isCategory:
        return Response({"error": "Category already exists"}, status=400)

    category = {"id": category_index, "name": name}
    categories[category_index] = category
    category_index += 1
    isCategory[name] = True
    return Response({"message": "Category created successfully", "category": category}, status=201)