#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import jsonpath
import traceback
import allure
from utils.set_log import Set_Log
from deepdiff import DeepDiff

log = Set_Log().log_info('check_result')


class Check_Result():

    def test_check_result(self,validate,response):
        """
        校验预期结果与实际结果是否一致
        """

        if response ==None:
            with allure.step("验证信息"):
                allure.attach(name="待核验信息", body=str(validate))
                allure.attach(name="检查模式", body=str(validate['check_mode']))
                allure.attach(name="预期响应码", body=str(validate['expected_code']))
                allure.attach(name="待核验字段信息", body=str(validate['expected_desc']))
                allure.attach(name="预期数据--数据格式", body=str(validate['expected_format']))
                allure.attach(name="实际数据", body=str(response))
                allure.attach(name="验证结果", body=str('通过' if validate == response else '失败'))


            assert validate == response
            log.info('\n待核验信息：{0} \n实际数据：{1} \n校验结果：'.format(validate,  response,('通过' if validate == response else '失败')))


        else:
            response = json.loads(response)

            if validate['check_mode'] == 'no_check':
                with allure.step("验证信息--不校验接口结果"):
                    pass


            elif validate['check_mode'] == 'check_code':
                expected_code = validate['expected_code']
                actual_code = response[0]

                with allure.step("验证信息--校验响应码"):
                    allure.attach(name="待核验信息", body=str(validate))
                    allure.attach(name="检查模式", body=str(validate['check_mode']))
                    allure.attach(name="预期响应码", body=str(validate['expected_code']))
                    allure.attach(name="实际响应码", body=str(response[0]))
                try:
                    assert str(expected_code) == str(actual_code)
                except AssertionError as e:
                    log.error('\n预期响应码:{0} \n实际响应码:{1} \n错误信息:{2}'.format(expected_code, actual_code,
                                                                                        traceback.format_exc()))
                    raise AssertionError('错误信息：{}'.format(traceback.format_exc()))
                log.info(
                    '\n待核验信息：{0} \n请求响应信息：{1} \n预期响应码：{2} \n实际响应码：{3}'.format(validate, response,
                                                                                                   expected_code,
                                                                                                   actual_code))


            elif validate['check_mode'] == 'check_desc':
                expected_desc = validate['expected_desc']
                for k, v in expected_desc.items():
                    expected_key = k
                    expected_value = v
                    actual_value = jsonpath.jsonpath(json.loads(response[1]), expected_key)
                    expected_v = [key for key in validate['expected_desc'].values()]

                with allure.step("验证信息--校验文本信息"):
                    allure.attach(name="待核验信息", body=str(validate))
                    allure.attach(name="检查模式", body=str(validate['check_mode']))
                    allure.attach(name="待核验字段信息", body=str(validate['expected_desc']))
                    allure.attach(name="等待验证文本信息", body=str(response[1]))
                    allure.attach(name="预期文本信息--值",
                                  body=str([key for key in validate['expected_desc'].values()][0]))
                    allure.attach(name="实际文本信息--值",
                                  body=str(False if actual_value == False else actual_value[0]))

                if actual_value == False:
                    try:
                        assert actual_value == True
                    except AssertionError as e:
                        log.error('\n关键字段key：{0} 未匹配到数据 \n匹配结果为：{1} \n错误信息:{2}'.format(expected_key,
                                                                                                          actual_value,
                                                                                                          traceback.format_exc()))
                        raise AssertionError(
                            '关键字段key：{0}未匹配到数据：{1}'.format(expected_key, traceback.format_exc()))
                else:
                    try:
                        assert expected_value == actual_value[0]
                    except AssertionError as e:
                        log.error('\n预期文本信息:{0} \n实际文本信息:{1} \n错误信息:{2}'.format(expected_value,
                                                                                                actual_value[0],
                                                                                                traceback.format_exc()))
                        raise AssertionError('错误信息：{}'.format(traceback.format_exc()))

                    log.info(
                        '\n待核验信息：{0} \n请求响应信息：{1} \n待核验字段信息：{2} \n等待验证文本信息：{3} \n预期文本信息:{4} \n实际文本信息:{5}'.format(
                            validate, response, expected_desc, response[1], expected_value, actual_value[0]))



            elif validate['check_mode'] == 'check_formt':
                expected_format = validate['expected_format']
                actual_format = json.loads(response[1])
                if isinstance(expected_format, dict) and isinstance(actual_format, dict):
                    cmp_dict = DeepDiff(expected_format, actual_format, ignore_order=True).to_dict()
                    cpm_result = cmp_dict.get('dictionary_item_added') or cmp_dict.get('dictionary_item_removed')
                    with allure.step("验证信息--校验数据格式"):
                        allure.attach(name="待核验信息", body=str(validate))
                        allure.attach(name="检查模式", body=str(validate['check_mode']))
                        allure.attach(name="预期数据--数据格式", body=str(validate['expected_format']))
                        allure.attach(name="实际数据--数据格式", body=str(response[1]))
                        allure.attach(name="数据格式校验结果", body=str('通过' if cpm_result == None else '失败'))

                    try:
                        if cpm_result:
                            assert expected_format == actual_format
                        else:
                            assert cpm_result == None

                    except AssertionError as e:
                        log.error('\n预期数据:{0} \n实际数据:{1} \n数据格式校验结果：{2} \n错误信息:{3}'.format(
                            expected_format, actual_format, cpm_result, traceback.format_exc()))
                        raise AssertionError('错误信息：{}'.format(traceback.format_exc()))

                    log.info(
                        '\n预期数据:{0} \n实际数据:{1} \n数据格式校验结果:{2}'.format(expected_format, actual_format,
                                                                                      cpm_result))

            else:
                log.info('预期结果与实际结果没有找到匹配的验证模式')


if __name__ == "__main__":
    validate = {'check_mode': 'check_desc', 'expected_code': 400, 'expected_desc': {'$..token_type': 'Bearer'},'expected_format': {"one": 1, "two": 2, "three":[3,4]}}
    response = [400, '{"code":101058,"success":false,"data":{},"msg":"门店车型代码重复！","token_type":"Bearer8"}']
    response1 = [400, '{"token_type":"Bearer88"}']

    c = Check_Result()
    res = c.test_check_result(validate,response)
