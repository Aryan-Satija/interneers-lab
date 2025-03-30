from ..serializers import CategorySerializer

class CategoryService:
    
    def create_category(self, data):
        serializer = CategorySerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return {"message": "Category Created Successfully", "category": serializer.data}, None
        
        return None, serializer.errors
