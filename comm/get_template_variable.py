#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from utils.operate_config import header_path,request_data_path
from utils.operate_json import Operate_Json

class Get_Template_Variable():

    def set_variable_data(self):
        """
        封装模板下的变量，即将请求头信息、请求数据封装为全局变量
        """
        dict_all = {}
        oj = Operate_Json(header_path)
        data = oj.read_json_data()

        oj2 = Operate_Json(request_data_path)
        data2 = oj2.read_json_data()

        dict_all.update(data)
        dict_all.update(data2)
        return dict_all




if __name__ == "__main__":
    g = Get_Template_Variable()
    res = g.set_variable_data()
    print(res)
