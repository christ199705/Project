from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Testsuits
from .serializers import TestsuitSerializer


# Create your views here.
class TestsuitView(ModelViewSet):
    queryset = Testsuits.objects.filter(is_delete=False)
    serializer_class = TestsuitSerializer
    lookup_field = "id"
    filter_backends = [OrderingFilter]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_detele = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
