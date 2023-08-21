#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from utils.operate_yaml import Operate_Yaml
from utils.operate_config import case_list_path,testcase_path

class Get_Testcase_Data():

    def get_testcase(self):
        """
        获取模块级别下的所有测试用例
        """
        case_list_run = []
        with open(case_list_path,'r',encoding='utf-8') as fp:
            for line in fp.readlines():
                data = str(line)
                if data != '' and not data.startswith("#"):
                    case_list_run.append(data.replace("\n", ""))

        oy = Operate_Yaml(testcase_path)
        datas = oy.read_yaml_template()

        case_list = []
        try:
            if case_list_run:
                for k in case_list_run:
                    data = datas[k]
                    case_list.append(data)

                res = [j for i in case_list for j in i]
                return res
            else:
                return None
        except KeyError as err:
            raise ('关键字key没有匹配到数据:\n{0}'.format(err))


    def get_testcase_run(self):
        """
        获取模块级别下 is_run == yes的测试用例
        """
        case_is_run = []
        cases = self.get_testcase()
        for case in cases:
            if case['is_run'] == True:
                case_is_run.append(case)
        return case_is_run



if __name__ == "__main__":
    g = Get_Testcase_Data()
    res = g.get_testcase()
    print(len(res),res)

    res2 = g.get_testcase_run()
    print(len(res2),res2)


