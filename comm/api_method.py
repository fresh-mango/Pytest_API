#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import time
import random
import requests
import json
import simplejson
import traceback
from requests_toolbelt import MultipartEncoder
from utils.operate_config import ParserConfig
from utils.set_log import Set_Log


log = Set_Log().log_info('api_method')


class Request_Method():
    """
    封装get、post请求
    """

    def post_main(self,url,data=None,headers=None ,mime_type=None, files=None,timeout=None ):
        res = None
        if headers != None:
            if 'application/json' in mime_type:
                res = requests.post(url=url, data=json.dumps(data),headers=headers,timeout=None ,verify=False)
                log.info("POST请求方法1: POST--application/json,请求响应信息：{0}".format(res.json()))

            elif 'form' in mime_type:
                res = requests.post(url=url, data=data, headers=headers,timeout=None, verify=False)
                log.info("POST请求方法2: POST--www-form-urlencoded,请求响应信息：{0}".format(res.json()))


            else:
                if 'multipart' in mime_type:
                    if files !=None:
                        if data!=None:
                            new_files = []
                            for key in files:
                                value = files[key]
                                # 判定参数值是否为文件，如果是则替换为二进制值
                                if '\\' in value:
                                    files[key] = (os.path.basename(value), open(value, 'rb'),
                                                  (os.path.splitext(value)[-1]).split('.')[-1])
                                    new_files.append(files[key])

                            res = requests.post(url=url, data=data, headers=headers, files=new_files, timeout=timeout,verify=False)
                            log.info("POST请求方法3: POST上传文件和数据--multpart/form-data,请求响应信息：{0}".format(res.json()))

                    else:
                        for key in files:
                            value = files[key]
                            # 判定参数值是否为文件，如果是则替换为二进制值
                            if '\\' in value:
                                files[key] = (os.path.basename(value), open(value, 'rb'))
                        multipart_encoder = MultipartEncoder(
                            fields=files,
                            boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
                        )
                        headers['Content-Type'] = multipart_encoder.content_type
                        res = requests.post(url=url, data=files, headers=headers, timeout=timeout,verify=False)
                        log.info("POST请求方法4: POST只上传文件--multipart/form-data,请求响应信息：{0}".format(res.json()))

        else:
            res = requests.post(url=url, data=data,timeout=None ,verify=False)
            log.info("POST请求方法5: POST-不携带请求头,请求响应信息：{0}".format(res.json()))



        try:
            if res.status_code != 200:
                return res.status_code, res.text
            else:
                return res.status_code, res.json()
        except json.decoder.JSONDecodeError:
            return res.status_code, None
        except simplejson.errors.JSONDecodeError:
            return res.status_code, None
        except Exception as e:
            log.error(traceback.format_exc())
            raise



    def get_main(self,url,data=None,header=None,timeout=None):
        res = None
        if header != None:
            res = requests.get(url=url, data=data, headers=header,timeout=None,verify=False)
            log.info("GET请求方法1: GET--携带请求头,请求响应信息：{0}".format(res.json()))

        else:
            res = requests.get(url=url, data=data,timeout=None,verify=False)
            log.info("GET请求方法2: GET--不携带请求头,请求响应信息：{0}".format(res.json()))


        if res.status_code == 301:
            res = requests.get(url=res.headers["location"], timeout=None,verify=False)
            log.info("请求响应码为重定向301，请求响应信息：{0}".format(res.json()))


        try:
            return res.status_code, res.json()
        except json.decoder.JSONDecodeError:
            return res.status_code, None
        except simplejson.errors.JSONDecodeError:
            return res.status_code, None
        except Exception as e:
            log.error(traceback.format_exc())
            raise


    def run_main(self,method,url,data=None,headers=None,mime_type=None,files=None):
        p = ParserConfig()
        interval = int(p.get_section_options('run_config', 'interval'))
        res = None
        if method == 'post':
            res = self.post_main(url,data,headers,mime_type,files)
        else:
            res = self.get_main(url,data,headers)

        time.sleep(interval)
        return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)


if __name__ == "__main__":
    url = "http://ldtest.xsdmt.com.cn/api/blade-auth/oauth/token?"
    data = {
        "tenantId": "329387",
        "username": "admin",
        "password": "670b14728ad9902aecba32e22fa4f6bd",
        "username": "admin",
        "grant_type": "password",
        "scope": "all",
        "type": "account"

    }
    header = {"Authorization": "Basic c2FiZXI6bGRAMTIzNDU2", "Tenant-Id": "683252"}
    rm = Request_Method()

    data = rm.run_main(method='post', url=url, data=data,headers = header,mime_type="application/json")
    data1 = json.loads(data)
    print(type(data1), data1)




