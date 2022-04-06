from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView

from user.serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
