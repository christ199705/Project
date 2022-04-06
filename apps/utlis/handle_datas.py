def handle_data2(datas):
    # 将【{ahe:18}】转化为【{key:"age",value:18,param_type:"int"}】
    result_list = []
    if datas is not None:
        for one_var_dict in datas:
            key = list(one_var_dict)[0]
            value = one_var_dict.get(key)
            result_list.append({
                "key": key,
                "value": value,
                "param_type": handle_param_type(value)
            })
    return result_list


def handle_param_type(value):
    if isinstance(value, int):
        param_type = "int"
    elif isinstance(value,float):
        param_type = "float"
    elif isinstance(value,bool):
        param_type = "boolean"
    else:
        param_type = "string"
    return param_type

