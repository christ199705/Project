import django_filters
from django.http import Http404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from interfaces.models import Interfaces
from .models import Projects
from .serializers import ProjectModelSerializer, ProjectByInterfacesSerializer, ByInterfacesSerializer
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from django.db.models import *
from .utils import get_count_by_project
from debugtalks.models import DebugTalks
from rest_framework import mixins

from rest_framework.generics import ListCreateAPIView

class ProjectView(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["id", "name"]
    ordering_fields = ["id","name"]

    # 重写删除项目
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 到这说明ID存在，但是判断下 ID是否已经被软删除了，如果软删除了报404
        if instance.is_delete is False:
            # debug文件也需要进行软删除
            debug = DebugTalks.objects.get(project=instance.id)
            debug.is_delete = True
            debug.save()

            instance.is_delete = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


        # 说明ID存在,但是已经被删除了
        else:
            raise Http404

    # 重写修改项目
    def update(self, request, *args, **kwargs):
        # 获取项目时，先判断该项目是否已经删除，如果已经删除，就返回404，就获取不到
        date = self.get_object()
        if date.is_delete is True:
            raise Http404
        return super().update(request, *args, **kwargs)

    # 重写获取单个项目
    def retrieve(self, request, *args, **kwargs):
        # 获取项目时，先判断该项目是否已经删除，如果已经删除，就返回404，就获取不到
        date = self.get_object()
        if date.is_delete is True:
            raise Http404
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(Projects.objects.filter(is_delete=False))
        #
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     # 把serializer.data 传入我的自定义函数，增加字段，然后返回新的data，data是字典格式
        #     data =
        #     return self.get_paginated_response(data)
        #
        # serializer = self.get_serializer(queryset, many=True)
        # # 把serializer.data 传入我的自定义函数，增加字段，然后返回新的data
        # data = get_count_by_project(serializer.data)
        # return Response(data)
        response = super().list(request, *args, **kwargs)
        response.data["results"] = get_count_by_project(response.data["results"])
        return response


    @action(methods=["get"], detail=True)
    # 通过Id查询所有接口信息
    def interfaces(self, request, id, **kwargs):
        # 通过ID获取接口信息，可以通过两个序例化器实现，也可以通过自己用ID去接口表里面查询的方式
        # interfaces_set = Interfaces.objects.filter(project=id)
        interfaces_set = self.get_object()
        serializer = ProjectByInterfacesSerializer(instance=interfaces_set)
        return Response(serializer.data)
