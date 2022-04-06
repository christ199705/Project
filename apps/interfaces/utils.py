import re
from testcases.models import Testcases
from configs.models import Configs


def update_date_time(data):
    date_time = re.search(r"^(.*)T(.*)\.", data["create_time"])
    data["create_time"] = date_time.group(1) + " " + date_time.group(2)
    return data


def update_list(datas):
    data_list = []
    for item in datas:
        time = re.search(r"^(.*?)T(.*?)\.", item["create_time"])
        item["create_time"] = time.group(1) + " " + time.group(2)

        testcase_num = Testcases.objects.filter(interfaces=item["id"]).count()

        config_num = Configs.objects.filter(interfaces=item["id"]).count()

        item["testcase_num"] = testcase_num
        item["config_num"] = config_num
        data_list.append(item)
    return data_list
