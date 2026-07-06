#users/views.py
from rest_framework.generics import CreateAPIView 
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [
        AllowAny,
    ]
