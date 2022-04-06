from django_filters.rest_framework import FilterSet
import django_filters
from .models import Envs


class ServerInfoFilter(FilterSet):
    """
    模糊查询
    """
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # icontains，包含且忽略大小写

    class Meta:
        # 指定模型
        models = Envs
        # 指定需要模糊查询的字段
        fields = ['name']