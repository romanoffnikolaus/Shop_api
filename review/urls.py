from django.urls import path, include
from .views import CommentView, CommentViewSet,  RatingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('rating', RatingViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]