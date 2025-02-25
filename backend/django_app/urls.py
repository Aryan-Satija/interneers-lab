from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    
    name = request.GET.get("name", "world")
    
    return JsonResponse({
        "status": True,
        "message": f"Hello {name}"
    })
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
]
