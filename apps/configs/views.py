from django.shortcuts import render
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Configs
# Create your views here.
from .serializers import ConfigSerializer
import json
from utlis.handle_datas import *
from interfaces.models import Interfaces


class ConfigView(ModelViewSet):
    queryset = Configs.objects.filter(is_delete=False)
    serializer_class = ConfigSerializer
    filter_backends = [OrderingFilter]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        config_obj = self.get_object()
        config_request = json.loads(config_obj.request)
        # 请求头数据
        config_headers = config_request["config"]["request"]["headers"]
        # variables全局变量数据
        config_variables = config_request["config"]["variables"]
        config_variables_list = handle_data2(config_variables)
        # name 的数据
        config_name = config_request["config"]["name"]
        selected_interface_id = config_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id

        datas = {
            "author": config_obj.author,
            "config_name": config_name,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
            "header": config_headers,
            "globalVar": config_variables_list
        }
        return Response(datas)
