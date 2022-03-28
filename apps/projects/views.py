from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from interfaces.models import Interfaces
from .models import Projects
from .serializers import ProjectModelSerializer, ProjectByInterfacesSerializer, ByInterfacesSerializer
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from django.db.models import *
from .utils import get_count_by_project

class ProjectView(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    lookup_field = "id"

    # 重写删除项目
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 到这说明ID存在，但是判断下 ID是否已经被软删除了，如果软删除了报404
        if instance.is_delete is False:
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
        queryset = Projects.objects.filter(is_delete=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = get_count_by_project(serializer.data)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = get_count_by_project(serializer.data)
        return Response(data)

    @action(methods=["get"], detail=True)
    # 通过Id查询所有接口信息
    def interfaces(self, request, id, **kwargs):
        interfaces_set = Interfaces.objects.filter(project=id)
        serializer = ByInterfacesSerializer(instance=interfaces_set, many=True)
        return Response(serializer.data)
