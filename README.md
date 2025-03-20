# Inventory Management System (Interneers' Lab)

## Description
This Inventory Management System is developed as part of Rippling's pre-internship program. The system facilitates efficient tracking and management of products to optimize stock control processes.

## Tech Stack
- **Frontend**: React.js (TypeScript)
- **Backend**: Django
- **Database**: MongoDB
- **Testing**: Python `unittest` for backend testing
- **Version Control**: Git & GitHub

## Installation  

#### Clone the Repository
```bash
git clone https://github.com/Aryan-Satija/interneers-lab.git
cd inventory-management-system
```
#### For Backend

```bash
cd backend
python -m venv venv
source ../venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### For Frontend
```bash
cd ../frontend
npm install
npm start
```

## API Documentation  

### 1. Get Product List  
**Endpoint:**  
```
GET /api/v1/product/
```
**Query Parameters:**  
- `page` (integer, optional, default: 1)  
- `page_size` (integer, optional, default: 10)  
- `sort_by` (string, optional)

**Response:**  
```json
{
    "page": 1,
    "pageSize": 10,
    "products": [
        {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 1200,
            "quantity": 5,
            "brand": 1,
            "category": 2
        }
    ]
}
```

---

### 2. Get Product Details  
**Endpoint:**  
```
GET /api/v1/product/{productId}/
```
**Path Parameter:**  
- `productId` (required): ID of the product  

**Response:**  
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1200,
    "quantity": 5,
    "brand": "hp",
    "category": "electronics"
}
```

---

### 3. Add a Product  
**Endpoint:**  
```
POST /api/v1/product/
```
**Request Body:**  
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1200,
    "quantity": 5,
    "brand": "67d6b556e19a4570777919f6",
    "category": "67d6b562e19a4570777919f8"
}
```
**Response:**  
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1200,
    "quantity": 5,
    "brand": "hp",
    "category": "electronics"
}
```

---

### 4. Update a Product  
**Endpoint:**  
```
PUT /api/v1/product/{productId}/
```
**Request Body:**  
```json
{
    "product": 1,
    "name": "Laptop",
    "description": "Updated description",
    "price": 1500,
    "quantity": 10,
    "brand": "67d6b556e19a4570777919f6",
    "category": "67d6b562e19a4570777919f8"
}
```
**Response:**  
```json
{
    "name": "Laptop",
    "description": "Updated description",
    "price": 1500,
    "quantity": 10,
    "brand": "hp",
    "category": "electronics"
}
```

---

### 5. Delete a Product  
**Endpoint:**  
```
DELETE /api/v1/product/{productId}/
```
**Request Body:**  
```json
{
    "product": "67d6b562e19a4570777919f8"
}
```
**Response:**  
```json
{
    "success": true
}
```

---

### 6. Add a Brand  
**Endpoint:**  
```
POST /api/v1/brand/
```
**Request Body:**  
```json
{
    "name": "Dell",
    "description": "Leading manufacturer of laptops and computers."
}
```
**Response:**  
```json
{
    "message": "Brand created successfully",
    "brand": {
        "id": 1,
        "name": "Dell",
        "description": "Leading manufacturer of laptops and computers."
    }
}
```

---

### 7. Add a Category  
**Endpoint:**  
```
POST /api/v1/category/
```
**Request Body:**  
```json
{
    "name": "Electronics",
    "description": "Devices and gadgets."
}
```
**Response:**  
```json
{
    "message": "Category created successfully",
    "category": {
        "id": 1,
        "name": "Electronics",
        "description": "Devices and gadgets."
    }
}
```
