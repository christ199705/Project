from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import RetrieveAPIView, GenericAPIView
# Create your views here.
from .models import DebugTalks
from .serializers import DebugtalkSerializer
from .filterset import ServerInfoFilter
from rest_framework import mixins


class DebugtalkView(mixins.ListModelMixin,mixins.UpdateModelMixin,GenericViewSet):
    queryset = DebugTalks.objects.filter(is_delete=False)
    serializer_class = DebugtalkSerializer
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    # ordering_fields = ["id", "name"]
    filterset_class = ServerInfoFilter

