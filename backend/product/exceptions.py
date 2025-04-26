class BrandNotFound(Exception):
    def __init__(self, brand_id=None):
        message = f"Brand not found."
        if brand_id:
            message += f" Brand ID: {brand_id}"
        else:
            message += f" Brand ID: None"
        super().__init__(message)

class ProductNotFound(Exception):
    def __init__(self, product_id=None):
        message = f"Product not found."
        if product_id:
            message += f" Product ID: {product_id}"
        else:
            message += f" Product ID: None"
        super().__init__(message)

class InvalidProductId(Exception):
    def __init__(self, product_id=None):
        message = f"Invalid product ID."
        if product_id:
            message += f" Provided: {product_id}"
        else:
            message += f" Provided: None"
        super().__init__(message)

class CategoryNotFound(Exception):
    def __init__(self, category_id=None):
        message = f"Category not found."
        if category_id:
            message += f" Category ID: {category_id}"
        else:
            message += f" Category ID: None"
        super().__init__(message)

class BrandValidationError(Exception):
    def __init__(self, details=None):
        message="Brand validation failed."
        if details:
            message += f" Details: {details}"
        super().__init__(message)

class ProductValidationError(Exception):
    def __init__(self, details=None):
        message="Product validation failed."
        if details:
            message += f" Details: {details}"
        super().__init__(message)

class CategoryValidationError(Exception):
    def __init__(self, details=None):
        message="Category validation failed."
        if details:
            message += f" Details: {details}"
        super().__init__(message)
