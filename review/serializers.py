from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Comment, Like, Rating, LikeCom


class CommentSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.count()
        return representation

    def create(self,validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment


class LikeSerializer(ModelSerializer):
    product = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Like
        fields = '__all__'
    
    def create(self,validated_data):
        request = self.context.get('request')
        user = request.user
        like = Like.objects.create(author=user, **validated_data)
        return like


class RatinfSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'
    
    def validate_rating(self, rating):
        if rating<0 or rating >5:
            raise serializers.ValidationError('Рейтинг 0-5')
        return rating
    
    def create(self,validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Rating.objects.create(author=user, **validated_data)
        return comment

    def validate_product(self, product):
        if self.Meta.model.objects.filter(product=product).exists():
            raise serializers.ValidationError('Вы можете оставить только один комментарий к данному товару')
        return product
    
    

class LikeCommentSerializer(ModelSerializer):
    comment = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = LikeCom
        fields = '__all__'
    
    def create(self,validated_data):
        request = self.context.get('request')
        user = request.user
        likecom = LikeCom.objects.create(author=user, **validated_data)
        return likecom