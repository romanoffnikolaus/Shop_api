from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, ProductViewset


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewset)

urlpatterns = [
    path('', include(router.urls))
]