import os.path
from django.utils.encoding import escape_uri_path
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from Project import settings
from .models import Reports
from .serializers import ReportSerializer
import re

from .utils import get_file


class ReportView(ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Reports.objects.filter(is_delete=False)
    filter_backends = [OrderingFilter]
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True)
    def download(self, request, id=None):
        instance = self.get_object()
        html = instance.html
        name = instance.name
        mach = re.search(r"(.*_)\d+", name)
        if mach:
            report_name = mach.group(1)
        else:
            report_name = name

        server_dir = settings.BASE_DIR.split("apps")[0]
        reports_dir = os.path.join(server_dir, "reports")
        reports_path = os.path.join(reports_dir, report_name)
        f = open(reports_path, "w+")
        f.write(html)
        f.close()
        response = StreamingHttpResponse(get_file(reports_path))
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = "attachment; filename={}".format(escape_uri_path(name))
        return response
