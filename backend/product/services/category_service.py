from ..serializers import CategorySerializer
from ..repository import categoryRepository, CategoryValidationError

class CategoryService:
    
    def create_category(self, data):
        serializer = CategorySerializer(data=data)
        
        if serializer.is_valid():
            try:
                categoryRepository.create_category(serializer.data)
            except Exception as e:
                raise e
        else:
            raise CategoryValidationError("Category data is invalid")