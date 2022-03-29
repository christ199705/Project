import re

from django.db.models import Count

from interfaces.models import Interfaces
from testsuits.models import Testsuits


def get_count_by_project(datas):
    data_list = []
    for item in datas:
        # 更改时间格式，通过正则表达式
        match = re.search(r"(.*)T(.*)\..*?", item["create_time"])
        item["create_time"] = match.group(1) + " " + match.group(2)

        # 获取这个项目的接口数量，直接查询
        interfaces_number = Interfaces.objects.filter(project=item["id"], is_delete=False).count()

        # 获取这个项目的所有测试集合数
        testsuit_number = Testsuits.objects.filter(project=item["id"], is_delete=False).count()

        # 获取这个项目下所有测试用例的数量,需要三个表的关联，需要分组等操作
        testcases = Interfaces.objects.values("id").annotate(testcases=Count("testcases")).filter(
            project=item["id"], is_delete=False)
        testcases_number = 0
        # 返回的是一个字典，需要遍历
        for i in testcases:
            testcases_number += i["testcases"]

        # 获取这个项目下的配置数量
        config = Interfaces.objects.values("id").annotate(config=Count("configs")). \
            filter(project=item["id"], is_delete=False)
        config_number = 0
        for i in config:
            config_number += i["config"]

        item["testsuit_number"] = testsuit_number
        item["interfaces_number"] = interfaces_number
        item["testcases_number"] = testcases_number
        item["config_number"] = config_number

        data_list.append(item)
    return data_list
