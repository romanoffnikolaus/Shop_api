from rest_framework.views import APIView
from .serilaizers import RegisterSerializer
from rest_framework.response import Response
from .models import User
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data #получить JSON
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Регистрация осуществлена', status=201)
    

class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first() #берем первого юзера
        if not user:
            return Response('Пользователь не найден', status=400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Активирован', status=200)
        
