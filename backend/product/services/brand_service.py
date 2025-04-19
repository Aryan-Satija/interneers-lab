from ..serializers import BrandSerializer
from ..repository import BrandRepository
from ..exceptions import BrandValidationError

brand_repository = BrandRepository()

class BrandService:
    
    def create_brand(self, data):
        serializer = BrandSerializer(data=data)
        
        if serializer.is_valid():
            brand_repository.create_brand(serializer.data)
        else:
            raise BrandValidationError("Category data is invalid")   

