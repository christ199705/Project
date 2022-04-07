import json

from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from interfaces.models import Interfaces
from .models import Testcases
from .serializers import TestcasesSerializer
from utlis.handle_datas import *


# Create your views here.
class TestcasesViewSet(ModelViewSet):
    queryset = Testcases.objects.filter(is_delete=False)
    serializer_class = TestcasesSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["id", "name"]

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        # 获取用例详情
        testcase_obj = self.get_object()

        #获取用例前置信息
        testcase_include = json.loads(testcase_obj.include)

        # 获取用例的请求信息
        testcase_request = json.loads(testcase_obj.request)
        testcase_request_datas = testcase_request.get("test").get("request")

        # 处理用例的Validatel列表

        # 将【{"check":"status_code","expected:200,"comparator":"eq"】转化为
        # {{key:"status_code",value:200,comparator:"eq",param_typr:"string "}}
        testcase_validate = testcase_request.get("test").get("validate")
        testcase_validate_list = handle_data1(testcase_validate)

        # 处理用例的param数据
        testcase_params = testcase_request_datas.get("params")
        testcase_params_list = handle_data4(testcase_params)

        # 处理用例的header列表
        testcase_headers = testcase_request_datas.get("headers")
        testcase_headers_list = handle_data4(testcase_headers)

        # 处理用例的variables变量列表
        testcase_variables = testcase_request_datas.get("test").get("variables")
        testcase_variables_list = handle_data2(testcase_variables)

        # 处理from表单数据
        testcase_from_datas = testcase_request_datas.get("datas")
        testcase_from_datas_list = handle_data6(testcase_from_datas)

        # 处理json数据
        testcase_json_datas = json.dumps(testcase_request_datas.get("json"),ensure_ascii=False)

        # 处理extract数据
        testcase_extract_datas = testcase_request.get("test").get("extract")
        testcase_extract_datas_list = handle_data3(testcase_extract_datas)

        # 处理extract数据
        testcase_parameters_datas = testcase_request.get("test").get("parameters")
        testcase_parameters_datas_list = handle_data3(testcase_parameters_datas)

        # 处理setup数据
        testcase_setup_hooks_datas = testcase_request.get("test").get("setup_hooks")
        testcase_setup_hooks_datas_list = handle_data5(testcase_setup_hooks_datas)

        # 处理teardown数据
        testcase_teardown_hooks_datas = testcase_request.get("test").get("teardown_hooks")
        testcase_teardown_hooks_datas_list = handle_data5(testcase_teardown_hooks_datas)

        selectd_config_id = testcase_include.get("config")
        selectd_interface_id = testcase_obj.interface_id
        selected_project_id = Interfaces.obkects.get(id=selectd_interface_id).project_id
        selected_testcase_id = testcase_include.get("testcase")

        datas = {
            "author":testcase_obj.author,
            "testcase_name":testcase_obj.name,
            "selectd_config_id":selectd_config_id,
            "selectd_interface_id":selectd_interface_id,
            "selected_project_id":selected_project_id,
            "selected_testcase_id":selected_testcase_id,

            "method":testcase_request_datas.get("method"),
            "url":testcase_request_datas.get("url"),
            "param":testcase_params_list,
            "header":testcase_headers_list,
            "variable":testcase_from_datas_list,
            "jsonVariable":testcase_json_datas,

            "extract":testcase_extract_datas_list,
            "validate":testcase_validate_list,
            "globalVar":testcase_variables_list,
            "parameterized":testcase_parameters_datas_list,
            "setupHooks":testcase_setup_hooks_datas_list,
            "teardownHooks":testcase_teardown_hooks_datas_list,
        }
        return Response(datas)