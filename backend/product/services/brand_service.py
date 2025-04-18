from ..serializers import BrandSerializer
from ..repository import BrandRepository, BrandValidationError
class BrandService:
    
    def create_category(self, data):
        serializer = BrandSerializer(data=data)
        
        if serializer.is_valid():
            try:
                BrandRepository.create_category(serializer.data)
            except Exception as e:
                raise e
        else:
            raise BrandValidationError("Category data is invalid")   

