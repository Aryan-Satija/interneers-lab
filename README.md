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
git clone <repository-url>
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
GET /getProductList/
```
**Query Parameters:**  
- `page` (integer, optional, default: 1)  
- `page_size` (integer, optional, default: 10)  

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
GET /getProduct/{productId}/
```
**Path Parameter:**  
- `productId` (integer, required): ID of the product  

**Response:**  
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1200,
    "quantity": 5,
    "brand": 1,
    "category": 2
}
```

---

### 3. Add a Product  
**Endpoint:**  
```
POST /addProduct/
```
**Request Body:**  
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1200,
    "quantity": 5,
    "brand": 1,
    "category": 2
}
```
**Response:**  
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1200,
    "quantity": 5,
    "brand": 1,
    "category": 2
}
```

---

### 4. Update a Product  
**Endpoint:**  
```
POST /updateProduct/
```
**Request Body:**  
```json
{
    "product": 1,
    "name": "Laptop",
    "description": "Updated description",
    "price": 1500,
    "quantity": 10,
    "brand": 1,
    "category": 2
}
```
**Response:**  
```json
{
    "name": "Laptop",
    "description": "Updated description",
    "price": 1500,
    "quantity": 10,
    "brand": 1,
    "category": 2
}
```

---

### 5. Delete a Product  
**Endpoint:**  
```
POST /deleteProduct/
```
**Request Body:**  
```json
{
    "product": 1
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
POST /addBrand/
```
**Request Body:**  
```json
{
    "name": "Dell"
}
```
**Response:**  
```json
{
    "message": "Brand created successfully",
    "brand": {
        "id": 1,
        "name": "Dell"
    }
}
```

---

### 7. Add a Category  
**Endpoint:**  
```
POST /addCategory/
```
**Request Body:**  
```json
{
    "name": "Electronics"
}
```
**Response:**  
```json
{
    "message": "Category created successfully",
    "category": {
        "id": 1,
        "name": "Electronics"
    }
}
```
