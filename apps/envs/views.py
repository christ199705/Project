from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from . import filterset
from .models import Envs
from rest_framework.viewsets import ModelViewSet
from .serializers import EnvSerializer


# Create your views here.
class EnvView(ModelViewSet):
    queryset = Envs.objects.filter(is_delete=False)
    serializer_class = EnvSerializer
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    # ordering_fields = ["id", "name"]
    filterset_class = filterset.ServerInfoFilter
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        pass
