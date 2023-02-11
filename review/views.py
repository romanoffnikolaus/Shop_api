from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Comment, Rating, LikeCom
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .serializers import CommentSerializer, RatinfSerializer, LikeCommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorOrReadOnly
# Create your views here.


class PermissioinMixin():
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated,]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorOrReadOnly,]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentViewSet(PermissioinMixin,ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(['POST'], detail=True) #detail false = для queryset
    def like(self, request, pk=None):
        comment = self.get_object()
        author = request.user
        serializer = LikeCommentSerializer(data=request.data) # в сериализатор передаем ДАТА. В аднном случае всегда реквест
        if serializer.is_valid(raise_exception=True):
            try:
                like = LikeCom.objects.get(comment=comment, author = author)
                like.delete()
                message = 'Dislike'
            except LikeCom.DoesNotExist:
                LikeCom.objects.create(comment=comment, is_liked=True, author = author)
                message = 'Like posted'
            return Response(message, status=200)


class RatingViewSet(PermissioinMixin,ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatinfSerializer


