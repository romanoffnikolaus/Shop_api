from django.shortcuts import render
from .models import Order
from rest_framework.viewsets import ModelViewSet
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated



class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]