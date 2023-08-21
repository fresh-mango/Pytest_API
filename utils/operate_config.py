#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import time
import os
import configparser

# 所有相关文件的路径
# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。
# 之前直接拼接的路径，修改了一下，用现在下面这种方法，可以支持linux和windows等不同的平台，也建议大家多用os.path.split()和os.path.join()，不要直接+'\\xxx\\ss'这样
base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
config_file = os.path.join(base_path, 'config', 'config.ini')
yaml_path = os.path.join(base_path, 'config','base_config.yaml')
case_list_path = os.path.join(base_path, 'config','case_list.txt')
header_path = os.path.join(base_path, 'config','header.json')
request_data_path = os.path.join(base_path, 'data','request_data.json')
testcase_path = os.path.join(base_path, 'data','testcase.yaml')
log_path = os.path.join(base_path, 'result','log')
report_path = os.path.join(base_path, 'result','report','html')


class ParserConfig():
    def load_ini(self):
        config = configparser.ConfigParser()
        config.read(config_file, encoding="utf-8-sig")
        return config

    #获取顶层路径
    def get_path(self):
        base_path =os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        return base_path

    #获取某个节点的全部配置项信息
    def get_section(self,node=None):
        if node == None:
            node = 'server'
        datas = self.load_ini()
        try:
            data = datas.options(node)
        except Exception:
            print("没有获取到配置节点信息")
            data = None
        return data

    # 获取单个节点的某项配置信息
    def get_section_options(self,node=None,key=None):
        if node == None:
            node = 'server'
            key='base_host'
        datas = self.load_ini()
        try:
            data = datas.get(node, key)
        except Exception:
            print("没有获取到配置节点选项信息")
            data = None
        return data


    #获取动态URL
    def get_url_parameter(self):
        scheme = self.get_section_options('server','scheme')
        host = self.get_section_options('server', 'host')
        port = self.get_section_options('server', 'port')
        host = scheme + '://' + host + '/'
        return host

    """------分割线-------获取[server]节点信息------"""
    #获取[server]节点--服务器IP
    def get_base_host(self):
        return self.get_section_options('server','base_host')

    #获取[server]节点--用户名
    def get_username(self):
        return self.get_section_options('server','username')

    #获取[server]节点--密码
    def get_password(self):
        return self.get_section_options('server','password')

    #获取[server]节点--租户ID
    def get_tenantId(self):
        return self.get_section_options('server','tenantId')


if __name__ == "__main__":
    pc = ParserConfig()
    data = pc.get_url_parameter()
    print(type(data),data)




