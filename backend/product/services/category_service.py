from ..serializers import CategorySerializer
from ..repository import CategoryRepository
from ..exceptions import CategoryValidationError

category_repository = CategoryRepository()

class CategoryService:
    
    def create_category(self, data):
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            category_repository.create_category(serializer.data)
        else:
            raise CategoryValidationError("Category data is invalid")