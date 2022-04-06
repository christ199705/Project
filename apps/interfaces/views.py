from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Interfaces
from .serializer import InterfaceSerializer, InterfacesTestcasesSerializers,InterfacesConfigsSerializers
from .utils import update_date_time, update_list
from testcases.models import Testcases


# Create your views here.

# 获取所有接口信息接口，需要返回用例数和配置数，时间进行格式化
# 删除为假删除
class InterfaceView(ModelViewSet):
    queryset = Interfaces.objects.filter(is_delete=False)
    serializer_class = InterfaceSerializer
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["id", "name"]
    ordering_fields = ["id", "name"]

    # 重写获取单个的方法
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = update_date_time(serializer.data)
        return Response(data)

    # 重写删除方法
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = update_list(serializer.data)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = update_list(serializer.data)
        return Response(data)

    @action(detail=True)
    def testcases(self, request, id, **kwargs):
        case = Testcases.objects.filter(interfaces=id, is_delete=False)
        # case = self.get_object()
        serializer = InterfacesTestcasesSerializers(instance=case, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def config(self, request, id, **kwargs):
        case = self.get_object()
        serializer = InterfacesConfigsSerializers(instance=case)
        return Response(serializer.data)
