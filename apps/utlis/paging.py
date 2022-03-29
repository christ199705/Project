from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict

class PageConfig(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    page_size_query_description = "每页几条"
    page_query_description = "第几页"

    def get_paginated_response(self, data):
        return Response(OrderedDict([

            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            # 数据
            ('results', data),
            # 总条数
            ('count', self.page.paginator.count),
            # 当前页数
            ('page_num', self.page.number),
            # 页数总条数
            ('total_page', self.page.paginator.num_pages),

        ]))