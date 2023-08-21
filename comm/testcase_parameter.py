#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import allure
import pytest
import json
import traceback
from comm.api_method import Request_Method
from comm.get_testcase_data import Get_Testcase_Data
from utils.set_log import Set_Log
from utils.operate_config import ParserConfig
from comm.check_result import Check_Result
from comm.dependent_data import Get_dependent_Data

log = Set_Log().log_info('testcase_info')
r = Request_Method()
cases= Get_Testcase_Data().get_testcase_run()
p = ParserConfig()
cr = Check_Result()
de = Get_dependent_Data()


@allure.epic("测试用例汇总")
@allure.feature("测试用例集合")
@allure.story("参数化--测试用例")
class Testcase_Suite():
    """
    封装get、post请求
    """
    @pytest.mark.parametrize('case', cases)
    def testcase_parameter(self,case):
        try:
            case_id = case['case_id']
            api_name = case['api_name']
            case_name = case['case_name']
            level = case['level']
            premise_caseid = case['premise_caseid']
            premise_key = case['premise_key']
            relevance_field = case['relevance_field']
            api_url = case['url']
            method = case['method']
            data = case['data']
            headers = case['headers']
            mime_type = case['mime_type']
            files = case['files']
            cookies = case['cookies']
            timeout = case['timeout']
            validate = case['validate']
            host = p.get_url_parameter()
            url = host + api_url




        except Exception as e:
            log.error(traceback.format_exc())
            raise KeyError('获取用例基本信息失败：{}'.format(e))

        log.info("*" * 200)
        log.info("用例id：%s" % str(case_id))
        log.info("接口名称：%s" % str(api_name))
        log.info("用例名称：%s" % str(case_name))
        log.info("前置用例：%s" % str(premise_caseid))
        log.info("前置用例响应数据：%s" % str(premise_key))
        log.info("数据依赖字段：%s" % str(relevance_field))
        log.info("api_url：%s" % str(api_url))
        log.info("请求地址：%s" % str(url))
        log.info("请求方式：%s" % str(method))
        log.info("请求数据：%s" % str(data))
        log.info("请求头信息：%s" % str(headers))
        log.info("参数媒体类型：%s" % str(mime_type))
        log.info("上传文件：%s" % str(files))
        log.info("cookies：%s" % str(cookies))
        log.info("超时时长：%s" % str(timeout))
        log.info("待核验信息：%s" % str(validate))



        if premise_caseid:
            with allure.step("前置条件："):
                allure.attach(name="前置条件--依赖caseid", body=str(premise_caseid))
                allure.attach(name="前置条件--依赖字段key", body=str(premise_key))
                allure.attach(name="前置条件--关联字段key", body=str(relevance_field))
                allure.dynamic.description(case_name)
                allure.dynamic.severity(level)
                allure.dynamic.title(api_name)
                allure.dynamic.description(case_name)
                allure.dynamic.link(name='百度首页地址', url='https://www.baidu.com/')

            response = de.get_dependent_case(case_id)

            with allure.step("请求数据信息："):
                allure.attach(name="请求地址", body=url)
                allure.attach(name="请求头信息", body=str(headers))
                allure.attach(name="请求数据", body=str(data))
                allure.attach(name="上传文件信息", body=str(files))
                allure.attach(name="请求数据响应信息", body=str( response if response==None else json.loads(response)))


            log.info('用例参数化--附带前置用例,请求响应信息:{0}'.format(response if response==None else json.loads(response)))

            cr.test_check_result(validate,response)


        else:
            response = r.run_main(method=method, url=url, data=data, headers=headers, mime_type=mime_type, files=files)

            with allure.step("请求数据信息："):
                allure.attach(name="请求地址", body=url)
                allure.attach(name="请求头信息", body=str(headers))
                allure.attach(name="请求数据", body=str(data))
                allure.attach(name="上传文件信息", body=str(files))
                allure.attach(name="请求响应信息", body=str(json.loads(response)))
                allure.dynamic.description(case_name)
                allure.dynamic.severity(level)
                allure.dynamic.title(api_name)

            log.info("\n请求响应信息： %s" % json.loads(response))
            cr.test_check_result(validate,response)




if __name__ == "__main__":
    c = Get_Testcase_Data()
    cases = c.get_testcase_run()[1]
    print('AAAAAAAAAA',cases)
    t = Testcase_Suite()
    t.testcase_parameter(cases)



