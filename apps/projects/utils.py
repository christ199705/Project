import re


def get_count_by_project(datas):
    data_list = []
    for item in datas:
        match = re.search(r"(.*)T(.*)\..*?", item["create_time"])
        item["create_time"] = match.group(1) + " " + match.group(2)
        data_list.append(item)
    return data_list
