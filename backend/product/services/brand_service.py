from ..serializers import BrandSerializer

class BrandService:
    @staticmethod
    def create_brand(data):
        serializer = BrandSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return {"message": "Brand Created Successfully", "brand": serializer.data}, None
        
        return None, serializer.errors
