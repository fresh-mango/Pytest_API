#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import yaml
from string import Template
from utils.operate_config import testcase_path
from comm.get_template_variable import Get_Template_Variable

class Operate_Yaml():
	def __init__(self, file_path=None):
		if file_path == None:
			self.file_path = testcase_path
		else:
			self.file_path = file_path
		self.data = self.read_yaml_data()

	def read_yaml_data(self):
		"""读取yaml文件数据
		:param yaml_file: yaml文件地址
		:return:
		"""
		with open(self.file_path,'r',encoding='utf-8') as f:
			return yaml.safe_load(f)


	def read_yaml_template(self,variable_data=None):
		"""读取带有变量的yaml文件数据，
		:param yaml_file: yaml文件地址
		:param variable_data: 变量数据
		:return:
		"""
		if variable_data == None:
			gv = Get_Template_Variable()
			data = gv.set_variable_data()
			variable_data =data

		else:
			variable_data = variable_data

		with open(self.file_path,'r',encoding='utf-8') as f:
			# return Template(f.read()).safe_substitute(variable_data)
			res = Template(f.read()).safe_substitute(variable_data)

			return yaml.safe_load(res)





	def write_yaml_file(self, data):
		"""把对象data写入yaml文件
		:param data: 数据对象
		:return:
		"""
		with open(self.file_path, 'w', encoding='utf-8') as f:
			return yaml.dump(data, f, Dumper=yaml.RoundTripDumper, allow_unicode=True)


	def get_data_section(self,section):
		return  self.read_yaml_data()[section]

if __name__ == "__main__":
	oy = Operate_Yaml()
	login = {'login': '张三55', 'age': 135}
	data = oy.read_yaml_template()
	print(type(data),data)
	# for i in data:
	# 	print(i)
