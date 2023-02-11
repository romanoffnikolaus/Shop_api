from rest_framework import serializers
from .models import User
from .utils import send_activation_code
from .tasks import send_activation_code_celery


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 4, required =True, write_only = True)
    password_confirm = serializers.CharField(min_length = 4, required =True, write_only = True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm') #необходиом удалить из АТТРС. POPвозвращает и удаляет
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery.delay(
            user.email, user.activation_code
        )
        return user
