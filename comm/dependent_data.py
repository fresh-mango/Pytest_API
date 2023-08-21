#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import  traceback
from comm.get_testcase_data import Get_Testcase_Data
from comm.api_method import Request_Method
from utils.operate_config import ParserConfig
from jsonpath_rw import jsonpath,parse
from utils.set_log import Set_Log
log = Set_Log().log_info('dependent_data')

r = Request_Method()
p = ParserConfig()

class Get_dependent_Data():

    def get_premise_case(self,case_id):
        """
        获取前置接口测试用例信息
        """
        t = Get_Testcase_Data()
        cases =t.get_testcase()
        for case in cases:
            if str(case['case_id']) == str(case_id):
                log.info('case_id:{0}，匹配到的case数据为:{1}'.format(case_id,case))
                return case
        return None


    def get_premise_request(self,case_id):
        """
        执行前置接口，获取响应信息
        """
        log.info('发送请求前，先获取用例case_id:{0}的case数据'.format(case_id))
        case = self.get_premise_case(case_id)
        if case !=None :
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
            response = r.run_main(method=method,url=url,data=data,headers=headers,mime_type=mime_type,files=files)
            res = json.loads(response)
            log.info('case_id: {0} ,请求响应信息:{1}'.format(case_id,res))
            return response


    def get_relevance_data(self,premise_caseid,premise_key):
        """
        执行前置接口,获取关联字段key的value
        """
        try:
            response = self.get_premise_request(premise_caseid)
            new_response = json.loads(response)[1]
            res = json.loads(new_response)
            json_exe = parse(premise_key)
            madle = json_exe.find(res)
            return [math.value for math in madle][0]

        except TypeError as e:
            print('字段 premise_key ：{0} 没有匹配到数据，错误信息:{1}'.format(premise_key,e))
        except IndexError as e:
            print('字段 premise_key ： {0} 没有匹配到数据，错误信息:{1}'.format(premise_key,e))
        except KeyError as e:
            print('字段 premise_key ：{0} 没有匹配到数据，错误信息:{1}'.format(premise_key,e))


    def get_dependent_case(self, case_id):
        """
        执行前置接口+替换关联变量+执行当前接口
        """
        case = self.get_premise_case(case_id)
        log.info('case_id:{0},用例信息:{1}'.format(case_id,case))
        if case :
            case_id = case['case_id']
            premise_caseid = case['premise_caseid']
            if premise_caseid !=None:
                log.info('第一层，if路径,case_id:{0},前置用例case_id:{1}'.format(case_id,premise_caseid))
                pre_case = self.get_premise_case(premise_caseid)
                if pre_case:
                    log.info('前置用例case_id:{0},用例信息:{1}'.format(premise_caseid,pre_case))
                    pre_case_id = pre_case['case_id']
                    pre_premise_caseid = pre_case['premise_caseid']
                    if pre_premise_caseid!=None:
                        log.info('第二层，if路径,case_id:{0},前置用例case_id:{1}'.format(pre_case_id, pre_premise_caseid))
                        pre_pre_case = self.get_premise_case(pre_premise_caseid)
                        if pre_pre_case :
                            log.info('前置用例case_id:{0},用例信息:{1}'.format(pre_premise_caseid, pre_pre_case))
                            pre_pre_case_id = pre_pre_case['case_id']
                            pre_pre_premise_caseid = pre_pre_case['premise_caseid']
                            if pre_pre_premise_caseid !=None:
                                log.info('第三层，if路径,case_id:{0},前置用例case_id:{1}'.format(pre_pre_case_id,pre_pre_premise_caseid))
                                case = self.get_premise_case(pre_pre_premise_caseid)
                                if case:
                                    case_id = case['case_id']
                                    premise_caseid = case['premise_caseid']
                                    premise_key = case['premise_key']
                                    relevance_field = case['relevance_field']
                                    api_url = case['url']
                                    method = case['method']
                                    data = case['data']
                                    headers = case['headers']
                                    mime_type = case['mime_type']
                                    files = case['files']
                                    host = p.get_url_parameter()
                                    url = host + api_url

                                    relevance_data = self.get_relevance_data(premise_caseid,premise_key)
                                    case['data'][relevance_field] = relevance_data

                                    response = r.run_main(method=method, url=url, data=data, headers=headers, mime_type=mime_type,files=files)
                                    res = json.loads(response)

                                    log.info('第四层，if路径,case_id:{0},前置用例case_id:{1},请求响应信息:{2}'.format(case_id, premise_caseid,res))
                                    return response


                                else:
                                    log.info('第三层，if路径,case_id:{0},前置用例case_id:{1},前置用例匹配结果:{2}'.format(pre_pre_case_id, pre_pre_premise_caseid, case))
                                    return case

                            else:
                                log.info('第三层，else路径,case_id:{0},前置用例case_id:{1}'.format(pre_pre_case_id,pre_pre_premise_caseid))
                                response = self.get_premise_request(pre_pre_case_id)
                                res = json.loads(response)
                                log.info('第三层，else路径，请求响应信息:{0}'.format(res))
                                return response


                        else:
                            log.info('第二层，if路径,case_id:{0},前置用例case_id:{1},前置用例匹配结果:{2}'.format(pre_case_id,pre_premise_caseid,pre_pre_case))
                            return pre_pre_case

                    else:
                        log.info('第二层，else路径,case_id:{0},前置用例case_id:{1}'.format(pre_case_id, pre_premise_caseid))
                        response = self.get_premise_request(pre_case_id)
                        res = json.loads(response)
                        log.info('第二层，else路径，请求响应信息:{0}'.format(res))
                        return response
                else:
                    log.info('第一层，if路径,case_id:{0},前置用例case_id:{1},前置用例匹配结果:{2}'.format(case_id, premise_caseid,pre_case))
                    return pre_case


            else:
                log.info('第一层，else路径,case_id:{0},前置用例case_id:{1}'.format(case_id,premise_caseid))
                response = self.get_premise_request(case_id)
                res = json.loads(response)
                log.info('第一层，else路径，请求响应信息:{0}'.format(res))
                return response
        else:
            return case


if __name__ == "__main__":

    g = Get_dependent_Data()
    res1 = g.get_dependent_case(4)
    print('结果：',res1)









